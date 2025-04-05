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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityWebviewBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val url = intent.getStringExtra("url") ?: "https://www.youtube.com"

        binding.webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
        }

        // 🔁 Her girişte çerez temizle
        CookieManager.getInstance().removeAllCookies(null)
        CookieManager.getInstance().flush()

        binding.webView.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView?, finishedUrl: String?) {
                super.onPageFinished(view, finishedUrl)

                if (finishedUrl != null && detectPlatform(finishedUrl) == "youtube") {
                    val cookieManager = CookieManager.getInstance()
                    val rawCookies = cookieManager.getCookie("https://www.youtube.com") ?: ""

                    // ✅ Gerekli çerezler kontrol listesi
                    val requiredCookies = listOf("SID", "HSID", "SSID", "PREF", "YSC")
                    val cookieMap = rawCookies.split(";").mapNotNull {
                        val parts = it.trim().split("=", limit = 2)
                        if (parts.size == 2) parts[0] to parts[1] else null
                    }.toMap()

                    val missingCookies = requiredCookies.filter { it !in cookieMap }

                    if (missingCookies.isEmpty()) {
                        // 🎯 Tüm çerezler varsa kaydet
                        getSharedPreferences("cookies", Context.MODE_PRIVATE)
                            .edit().putString("cookies_youtube", rawCookies).apply()

                        val resultIntent = Intent().apply {
                            putExtra("platform", "youtube")
                            putExtra("cookies", rawCookies)
                        }

                        setResult(RESULT_OK, resultIntent)
                        Toast.makeText(this@WebViewActivity, "Çerezler alındı ✅", Toast.LENGTH_SHORT).show()
                        finish()
                    } else {
                        Toast.makeText(
                            this@WebViewActivity,
                            "Eksik çerezler: ${missingCookies.joinToString(", ")}",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                }
            }
        }

        binding.webView.loadUrl(url)
    }

    private fun detectPlatform(url: String): String? {
        return when {
            url.contains("youtube.com") || url.contains("google.com") -> "youtube"
            url.contains("instagram.com") -> "instagram"
            url.contains("twitter.com") || url.contains("x.com") -> "twitter"
            else -> null
        }
    }
}
