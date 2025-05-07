package com.example.downloadmateapp.service

import android.app.*
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.IBinder
import androidx.core.app.NotificationCompat
import androidx.core.content.FileProvider
import com.example.downloadmateapp.R
import com.example.downloadmateapp.api.RetrofitClient
import com.example.downloadmateapp.helper.DownloadHelper
import com.example.downloadmateapp.helper.PrefsHelper
import com.example.downloadmateapp.network.DownloadRequest
import kotlinx.coroutines.*
import java.io.File

class DownloadService : Service() {

    private val serviceScope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val url = intent?.getStringExtra("url")
        val platform = intent?.getStringExtra("platform")
        val type = intent?.getStringExtra("type")
        val fileNameInput = intent?.getStringExtra("fileName")?.takeIf { it.isNotBlank() } ?: ""

        if (url.isNullOrBlank() || platform.isNullOrBlank() || type.isNullOrBlank()) {
            return stopAndExit()
        }

        startForeground(1, createNotification("İndirme başladı"))

        serviceScope.launch {
            try {
                val request = DownloadRequest(url = url, type = type)

                val cookies = getSharedPreferences("cookies", Context.MODE_PRIVATE)
                    .getString("cookies_$platform", null)

                val cookiePlatforms = listOf("youtube", "instagram", "twitter")
                if (platform in cookiePlatforms && cookies.isNullOrEmpty()) {
                    log("Gerekli cookie eksik: $platform")
                    return@launch
                }

                val response = when (platform) {
                    "youtube" -> RetrofitClient.apiService.downloadYoutube(request, cookies)
                    "instagram" -> RetrofitClient.apiService.downloadInstagram(request, cookies)
                    "twitter" -> RetrofitClient.apiService.downloadTwitter(request, cookies)
                    "tiktok" -> RetrofitClient.apiService.downloadTiktok(request)
                    "facebook" -> RetrofitClient.apiService.downloadFacebook(request)
                    else -> null
                }

                if (response?.isSuccessful == true) {
                    val body = response.body()
                    val language = PrefsHelper.get(this@DownloadService, "selected_language", "tr")

                    if (body != null) {
                        val fileNameFromApi = extractFileName(response.headers()["Content-Disposition"])
                        val finalFileName = buildFinalFileName(fileNameFromApi, fileNameInput)

                        val savedFile = DownloadHelper.saveToDownloadMateFolder(
                            body,
                            finalFileName,
                            this@DownloadService,
                            language
                        )

                        if (savedFile != null) {
                            log("✅ İndirme tamamlandı: ${savedFile.absolutePath}")
                            showCompletionNotification(savedFile)
                        } else {
                            log("❌ Dosya kaydedilemedi.")
                        }
                    }
                } else {
                    val errorMsg = response?.errorBody()?.string()
                    log("❌ İndirme başarısız: $errorMsg")
                }

            } catch (e: Exception) {
                log("🚨 Hata oluştu: ${e.message}")
            } finally {
                stopAndExit()
            }
        }

        return START_NOT_STICKY
    }

    override fun onDestroy() {
        serviceScope.cancel()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun createNotification(message: String): Notification {
        val channelId = "download_channel"
        val channelName = "İndirme Bildirimi"
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            val channel = NotificationChannel(channelId, channelName, NotificationManager.IMPORTANCE_LOW)
            manager.createNotificationChannel(channel)
        }

        return NotificationCompat.Builder(this, channelId)
            .setContentTitle("DownloadMate")
            .setContentText(message)
            .setSmallIcon(R.drawable.ic_downloads)
            .build()
    }

    private fun showCompletionNotification(file: File) {
        val channelId = "download_complete_channel"
        val channelName = "İndirme Tamamlandı"
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // 🔐 Android 13+ için: POST_NOTIFICATIONS izni kontrolü yapılmadan bu bildirim gösterilmez
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            if (checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                log("🚫 POST_NOTIFICATIONS izni yok, bildirim gösterilmedi.")
                return
            }
        }

        // ✅ Bildirim kanalını oluştur
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            val channel = NotificationChannel(channelId, channelName, NotificationManager.IMPORTANCE_DEFAULT).apply {
                description = "İndirme tamamlandığında kullanıcıya bildirim gösterilir."
            }
            manager.createNotificationChannel(channel)
        }

        // ✅ Dosyayı açmak için PendingIntent oluştur
        val uri: Uri = FileProvider.getUriForFile(
            this,
            "${applicationContext.packageName}.provider",
            file
        )

        val openIntent = Intent(Intent.ACTION_VIEW).apply {
            setDataAndType(uri, contentResolver.getType(uri))
            flags = Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_ACTIVITY_NEW_TASK
        }

        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        // ✅ Bildirimi oluştur ve göster
        val notification = NotificationCompat.Builder(this, channelId)
            .setContentTitle("İndirme Tamamlandı")
            .setContentText(file.name)
            .setSmallIcon(R.drawable.ic_downloads) // ⚠️ ic_download_done yoksa güvenli simgeyi kullan
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        log("📣 Bildirim gösteriliyor: ${file.name}")
        manager.notify(System.currentTimeMillis().toInt(), notification)
    }


    private fun extractFileName(contentDisposition: String?): String {
        return contentDisposition?.substringAfter("filename=")?.replace("\"", "")
            ?: "indirilen_dosya_${System.currentTimeMillis()}.tmp"
    }

    private fun buildFinalFileName(apiFileName: String, userInput: String): String {
        return if (userInput.isNotBlank()) {
            val extension = apiFileName.substringAfterLast('.', "tmp")
            val safeName = userInput.replace(Regex("[^a-zA-Z0-9._-]"), "_")
            "$safeName.$extension"
        } else {
            apiFileName
        }
    }

    private fun stopAndExit(): Int {
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
        return START_NOT_STICKY
    }

    private fun log(msg: String) {
        android.util.Log.d("DownloadService", msg)
    }
}
