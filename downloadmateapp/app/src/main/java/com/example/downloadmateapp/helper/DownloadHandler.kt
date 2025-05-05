package com.example.downloadmateapp.helper

import android.content.Context
import android.view.View
import androidx.lifecycle.LifecycleCoroutineScope
import com.example.downloadmateapp.R
import com.example.downloadmateapp.api.RetrofitClient
import com.example.downloadmateapp.network.DownloadRequest
import okhttp3.ResponseBody
import java.io.File

object DownloadHandler {

    fun handleDownload(
        context: Context,
        lifecycleScope: LifecycleCoroutineScope,
        url: String,
        platform: String,
        type: String,
        fileNameInput: String,
        progressBar: View,
        onSuccess: (File) -> Unit,
        onError: (String) -> Unit,
        onClearInputs: () -> Unit
    ) {
        if (platform.isBlank() || type == "seçiniz" || url.isBlank()) {
            ToastHelper.show(context, R.string.msg_fill_all_fields)
            return
        }

        progressBar.visibility = View.VISIBLE
        val request = DownloadRequest(url = url, type = type)

        // Cookie gerektiren platformlar burada tanımlanır
        val platformsRequiringCookies = listOf("youtube", "instagram", "twitter")

        lifecycleScope.launchWhenStarted {
            try {
                val cookies = context.getSharedPreferences("cookies", Context.MODE_PRIVATE)
                    .getString("cookies_$platform", null)

                if (platform in platformsRequiringCookies && cookies.isNullOrEmpty()) {
                    ToastHelper.long(context, R.string.msg_cookie_missing, platform)
                    progressBar.visibility = View.GONE
                    return@launchWhenStarted
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
                    val contentDisposition = response.headers()["Content-Disposition"]
                    val body = response.body()
                    if (body != null) {
                        val savedFile = DownloadHelper.saveToDownloadMateFolder(
                            body,
                            extractFileName(contentDisposition),
                            context,
                            PrefsHelper.get(context, "selected_language", "tr")
                        )
                        val renamed = DownloadHelper.renameIfNeeded(savedFile!!, fileNameInput)
                        onSuccess(renamed)
                        onClearInputs()
                    }
                } else {
                    val msg = response?.errorBody()?.string() ?: "Bilinmeyen hata"
                    onError(msg)
                }

            } catch (e: Exception) {
                onError(e.message ?: "Hata")
            } finally {
                progressBar.visibility = View.GONE
            }
        }
    }

    private fun extractFileName(contentDisposition: String?): String {
        return contentDisposition?.substringAfter("filename=")?.replace("\"", "")
            ?: "indirilen_dosya_${System.currentTimeMillis()}.tmp"
    }
}