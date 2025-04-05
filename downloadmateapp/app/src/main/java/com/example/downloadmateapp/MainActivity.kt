package com.example.downloadmateapp

import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.view.Menu
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.appcompat.widget.SwitchCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.downloadmateapp.databinding.ActivityMainBinding
import androidx.lifecycle.lifecycleScope
import com.example.downloadmateapp.api.RetrofitClient
import com.example.downloadmateapp.network.DownloadRequest
import kotlinx.coroutines.launch
import okhttp3.ResponseBody
import java.io.File
import java.io.FileOutputStream
import java.io.InputStream

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var folderPickerLauncher: androidx.activity.result.ActivityResultLauncher<Intent>
    private lateinit var webViewLauncher: androidx.activity.result.ActivityResultLauncher<Intent>

    companion object {
        private const val PREFS_NAME = "app_preferences"
        private const val KEY_THEME_MODE = "theme_mode"
        private const val PREF_KEY_FOLDER_URI = "selected_folder_uri"
        private const val PREF_KEY_GALLERY_PERMISSION = "allow_gallery_save"
        private const val GALLERY_PREF_CHECKED_KEY = "gallery_pref_checked"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Launcher - WebView
        webViewLauncher = registerForActivityResult(
            androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult()
        ) { result ->
            if (result.resultCode == RESULT_OK) {
                val platform = result.data?.getStringExtra("platform") // gelen platform adı
                val cookies = result.data?.getStringExtra("cookies")
                if (!cookies.isNullOrEmpty() && !platform.isNullOrEmpty()) {
                    getSharedPreferences("cookies", Context.MODE_PRIVATE)
                        .edit()
                        .putString("cookies_$platform", cookies)
                        .apply()
                    Toast.makeText(this, "$platform çerezi alındı ✅", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this, "Çerez alınamadı ❌", Toast.LENGTH_SHORT).show()
                }

            }
        }

        // Launcher - Klasör Seçici
        folderPickerLauncher = registerForActivityResult(
            androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult()
        ) { result ->
            if (result.resultCode == RESULT_OK) {
                val folderUri = result.data?.data ?: return@registerForActivityResult
                contentResolver.takePersistableUriPermission(folderUri, Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
                getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
                    .edit()
                    .putString(PREF_KEY_FOLDER_URI, folderUri.toString())
                    .apply()
                Toast.makeText(this, "📁 Kayıt klasörü seçildi", Toast.LENGTH_SHORT).show()
            }
        }

        // Tema ayarları
        val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        AppCompatDelegate.setDefaultNightMode(
            prefs.getInt(KEY_THEME_MODE, AppCompatDelegate.MODE_NIGHT_NO)
        )

        // Galeri tercihi sorulmamışsa sor
        if (!prefs.getBoolean(GALLERY_PREF_CHECKED_KEY, false)) {
            android.app.AlertDialog.Builder(this)
                .setTitle("Galeri Kaydı")
                .setMessage("MP4 dosyaları galeriye kaydedilsin mi?")
                .setPositiveButton("Evet") { _, _ ->
                    prefs.edit().putBoolean(PREF_KEY_GALLERY_PERMISSION, true)
                        .putBoolean(GALLERY_PREF_CHECKED_KEY, true).apply()
                }
                .setNegativeButton("Hayır") { _, _ ->
                    prefs.edit().putBoolean(PREF_KEY_GALLERY_PERMISSION, false)
                        .putBoolean(GALLERY_PREF_CHECKED_KEY, true).apply()
                }
                .show()
        }

        // UI bağlantıları
        setSupportActionBar(binding.topAppBar)
        setupSpinners()
        setSocialIconsForTheme()

        binding.buttonInstagram.setOnClickListener {
            openWebView("https://www.instagram.com/accounts/login/")
        }

        binding.buttonYouTube.setOnClickListener {
            openWebView("https://www.youtube.com/feed/subscriptions")
        }

        binding.buttonTwitter.setOnClickListener {
            openWebView("https://twitter.com/i/flow/login")
        }



        binding.buttonDownload.setOnClickListener {
            val url = binding.editTextUrl.text.toString()
            val platform = binding.spinnerPlatform.selectedItem.toString().lowercase()
            val type = binding.spinnerType.selectedItem.toString().lowercase()

            if (platform == "seçiniz" || type == "seçiniz" || url.isBlank()) {
                Toast.makeText(this, "⚠️ Lütfen tüm alanları doldurun", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            binding.progressBar.visibility = View.VISIBLE
            val request = DownloadRequest(url = url, type = type)

            lifecycleScope.launch {
                try {
                    val cookies = getSharedPreferences("cookies", Context.MODE_PRIVATE)
                        .getString("cookies_$platform", null)

                    if (cookies.isNullOrEmpty()) {
                        Toast.makeText(this@MainActivity, "Lütfen önce $platform hesabınıza giriş yaparak çerez alın!", Toast.LENGTH_LONG).show()
                        binding.progressBar.visibility = View.GONE
                        return@launch
                    }

                    val response = when (platform) {
                        "youtube" -> RetrofitClient.apiService.downloadYoutube(request, cookies)
                        "instagram" -> RetrofitClient.apiService.downloadInstagram(request, cookies)
                        "twitter" -> RetrofitClient.apiService.downloadTwitter(request, cookies)
                        else -> null
                    }

                    if (response?.isSuccessful == true) {
                        val contentDisposition = response.headers()["Content-Disposition"]
                        val body = response.body()
                        if (body != null) {
                            val savedFile = saveFileWithPreferences(body, contentDisposition, this@MainActivity, type)
                            if (savedFile != null) {
                                val customName = binding.editTextFileName.text.toString().trim()
                                    .replace(Regex("[^a-zA-Z0-9._-]"), "_")

                                val finalFile = if (customName.isNotEmpty() && customName.length <= 40) {
                                    val renamed = File(savedFile.parent, "$customName.${savedFile.extension}")
                                    savedFile.renameTo(renamed)
                                    renamed
                                } else savedFile

                                Toast.makeText(this@MainActivity, "✅ Kaydedildi: ${finalFile.name}", Toast.LENGTH_LONG).show()
                            }
                        }

                        // 🎯 Alanları temizle
                        binding.editTextUrl.text.clear()
                        binding.editTextFileName.text.clear()
                        binding.spinnerPlatform.setSelection(0)
                        binding.spinnerType.setSelection(0)

                    } else {
                        val msg = response?.errorBody()?.string() ?: "Bilinmeyen hata"
                        Toast.makeText(this@MainActivity, "❗API Hatası: $msg", Toast.LENGTH_LONG).show()
                    }

                } catch (e: Exception) {
                    Toast.makeText(this@MainActivity, "❗ Hata: ${e.message}", Toast.LENGTH_SHORT).show()
                } finally {
                    binding.progressBar.visibility = View.GONE
                }
            }
        }

        binding.buttonOpenDownload.setOnClickListener {
            try {
                val downloadsDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
                val appFolder = File(downloadsDir, "DownloadMateDownloads")

                if (!appFolder.exists()) {
                    Toast.makeText(this, "Klasör bulunamadı.", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }

                val intent = Intent(Intent.ACTION_VIEW).apply {
                    setDataAndType(Uri.fromFile(appFolder), "resource/folder")
                    flags = Intent.FLAG_ACTIVITY_NEW_TASK
                }

                startActivity(intent)

            } catch (e: Exception) {
                e.printStackTrace()
                Toast.makeText(this, "❗ Klasör açılamadı", Toast.LENGTH_SHORT).show()
            }
        }

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    private fun openWebView(url: String) {
        val intent = Intent(this, WebViewActivity::class.java)
        intent.putExtra("url", url)
        webViewLauncher.launch(intent)
    }

    private fun saveFileWithPreferences(
        responseBody: ResponseBody,
        contentDisposition: String?,
        context: Context,
        type: String
    ): File? {
        val fileName = contentDisposition?.substringAfter("filename=")?.replace("\"", "")
            ?: "indirilen_dosya_${System.currentTimeMillis()}.tmp"

        return saveToDownloadMateFolder(responseBody, fileName, context)
    }




    private fun saveToGallery(responseBody: ResponseBody, fileName: String, context: Context) {
        val contentValues = android.content.ContentValues().apply {
            put(android.provider.MediaStore.Video.Media.DISPLAY_NAME, fileName)
            put(android.provider.MediaStore.Video.Media.MIME_TYPE, "video/mp4")
            put(android.provider.MediaStore.Video.Media.RELATIVE_PATH, "Movies/DownloadMateApp") // 🎯 özel klasör
        }

        val uri = contentResolver.insert(
            android.provider.MediaStore.Video.Media.EXTERNAL_CONTENT_URI,
            contentValues
        )

        if (uri != null) {
            try {
                contentResolver.openOutputStream(uri)?.use { output ->
                    responseBody.byteStream().use { input -> input.copyTo(output) }
                }

                val msg = "🎬 Galeriye kaydedildi: Movies/DownloadMateApp/$fileName"
                Toast.makeText(context, msg, Toast.LENGTH_SHORT).show()
                android.util.Log.d("DownloadMate", msg)

            } catch (e: Exception) {
                e.printStackTrace()
                Toast.makeText(context, "❗ Galeriye kaydedilemedi", Toast.LENGTH_SHORT).show()
            }
        } else {
            Toast.makeText(context, "❗ Galeriye URI alınamadı", Toast.LENGTH_SHORT).show()
        }
    }



    private fun saveToCustomFolder(
        responseBody: ResponseBody,
        fileName: String,
        folderUri: Uri,
        context: Context
    ): File? {
        return try {
            val docUri = android.provider.DocumentsContract.createDocument(
                contentResolver,
                folderUri,
                "application/octet-stream",
                fileName
            )
            docUri?.let {
                contentResolver.openOutputStream(it)?.use { output ->
                    responseBody.byteStream().use { input -> input.copyTo(output) }
                }
            }

            val msg = "📁 Özel klasöre kaydedildi"
            Toast.makeText(context, msg, Toast.LENGTH_SHORT).show()
            android.util.Log.d("DownloadMate", msg)

            null // ContentResolver üzerinden kaydettik, fiziksel dosya objesi dönmüyoruz
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(context, "❗ Klasöre kaydedilirken hata oluştu", Toast.LENGTH_SHORT).show()
            null
        }
    }



    private fun saveToDownloadMateFolder(
        responseBody: ResponseBody,
        fileName: String,
        context: Context
    ): File? {
        return try {
            val downloadsDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
            val appFolder = File(downloadsDir, "DownloadMateDownloads")
            if (!appFolder.exists()) appFolder.mkdirs()

            val file = File(appFolder, fileName)
            val inputStream = responseBody.byteStream()
            val outputStream = FileOutputStream(file)
            inputStream.use { it.copyTo(outputStream) }

            val msg = "💾 İndirilenler'e kaydedildi: ${file.absolutePath}"
            Toast.makeText(context, msg, Toast.LENGTH_SHORT).show()
            android.util.Log.d("DownloadMate", msg)

            file
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(context, "❗ Dosya kaydedilirken hata oluştu", Toast.LENGTH_SHORT).show()
            null
        }
    }





    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.toolbar_menu, menu)
        val toggleItem = menu?.findItem(R.id.action_toggle_theme)
        val switch = toggleItem?.actionView as? SwitchCompat
        val isDark = isNightMode()
        switch?.isChecked = isDark
        val thumbColor = if (isDark) Color.WHITE else Color.BLACK
        val trackColor = if (isDark) Color.LTGRAY else Color.DKGRAY
        switch?.apply {
            setBackgroundColor(Color.TRANSPARENT)
            thumbDrawable?.setTint(thumbColor)
            trackDrawable?.setTint(trackColor)
            setOnCheckedChangeListener { _, isChecked ->
                val mode = if (isChecked) AppCompatDelegate.MODE_NIGHT_YES else AppCompatDelegate.MODE_NIGHT_NO
                AppCompatDelegate.setDefaultNightMode(mode)
                getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
                    .edit().putInt(KEY_THEME_MODE, mode).apply()
                setSocialIconsForTheme()
            }
        }
        return true
    }

    private fun isNightMode(): Boolean {
        val currentNightMode = resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK
        return currentNightMode == Configuration.UI_MODE_NIGHT_YES
    }

    private fun setSocialIconsForTheme() {
        val isDark = isNightMode()
        val instagramIcon = if (isDark) R.drawable.ic_d_instagram else R.drawable.ic_instagram
        val youtubeIcon = if (isDark) R.drawable.ic_d_youtube else R.drawable.ic_youtube
        val twitterIcon = if (isDark) R.drawable.ic_d_twitter else R.drawable.ic_twitter

        binding.buttonInstagram.setImageResource(instagramIcon)
        binding.buttonYouTube.setImageResource(youtubeIcon)
        binding.buttonTwitter.setImageResource(twitterIcon)

        if (!isDark) {
            val white = getColor(android.R.color.white)
            binding.buttonInstagram.setColorFilter(white)
            binding.buttonYouTube.setColorFilter(white)
            binding.buttonTwitter.setColorFilter(white)
        } else {
            binding.buttonInstagram.imageTintList = null
            binding.buttonYouTube.imageTintList = null
            binding.buttonTwitter.imageTintList = null
        }
    }

    private fun setupSpinners() {
        val platforms = listOf("Seçiniz", "YouTube", "Instagram", "Twitter")
        val types = listOf("Seçiniz", "Video", "Audio")

        binding.spinnerPlatform.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, platforms)
            .also { it.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item) }

        binding.spinnerType.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, types)
            .also { it.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item) }

        binding.spinnerPlatform.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>, view: View?, pos: Int, id: Long) {
                val selected = parent.getItemAtPosition(pos).toString().lowercase()
                when (selected) {
                    "youtube" -> binding.buttonDownload.setBackgroundColor(Color.parseColor("#FF0000"))
                    "twitter" -> binding.buttonDownload.setBackgroundColor(Color.parseColor("#1DA1F2"))
                    "instagram" -> binding.buttonDownload.setBackgroundColor(Color.parseColor("#c13584"))
                    "seçiniz" -> {
                        val defaultColor = if (isNightMode()) Color.WHITE else Color.BLACK
                        val textColor = if (isNightMode()) Color.BLACK else Color.WHITE
                        binding.buttonDownload.setBackgroundColor(defaultColor)
                        binding.buttonDownload.setTextColor(textColor)
                    }
                }
            }

            override fun onNothingSelected(parent: AdapterView<*>) {}
        }
    }
}
