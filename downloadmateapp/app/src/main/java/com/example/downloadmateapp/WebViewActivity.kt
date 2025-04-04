package com.example.downloadmateapp

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.webkit.CookieManager
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.downloadmateapp.databinding.ActivityWebviewBinding

class WebViewActivity : AppCompatActivity() {

    private lateinit var binding: ActivityWebviewBinding
    private var cookiesSaved = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityWebviewBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val url = intent.getStringExtra("url") ?: "https://www.google.com"

        binding.webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
        }

        binding.webView.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView?, finishedUrl: String?) {
                super.onPageFinished(view, finishedUrl)

                if (!cookiesSaved && finishedUrl != null && shouldCaptureCookies(finishedUrl)) {
                    val cookieManager = CookieManager.getInstance()
                    val cookies = cookieManager.getCookie(finishedUrl)

                    if (!cookies.isNullOrBlank()) {
                        cookiesSaved = true

                        val platform = detectPlatform(finishedUrl)
                        if (platform != null) {
                            val prefs = getSharedPreferences("cookies", Context.MODE_PRIVATE)
                            prefs.edit().putString("cookies_$platform", cookies).apply()

                            val resultIntent = Intent().apply {
                                putExtra("platform", platform)
                                putExtra("cookies", cookies)
                            }

                            setResult(RESULT_OK, resultIntent)

                            Toast.makeText(
                                this@WebViewActivity,
                                "$platform çerezleri kaydedildi ✅",
                                Toast.LENGTH_SHORT
                            ).show()

                            finish()
                        }
                    }
                }
            }
        }

        binding.webView.loadUrl(url)
    }

    private fun shouldCaptureCookies(url: String): Boolean {
        return detectPlatform(url) != null
    }

    private fun detectPlatform(url: String): String? {
        return when {
            url.contains("instagram.com") -> "instagram"
            url.contains("youtube.com") || url.contains("google.com") -> "youtube"
            url.contains("twitter.com") || url.contains("x.com") -> "twitter"
            else -> null
        }
    }
}
