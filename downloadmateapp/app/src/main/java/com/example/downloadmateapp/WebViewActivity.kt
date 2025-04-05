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

        val url = intent.getStringExtra("url") ?: "https://www.google.com"
        val platform = detectPlatform(url) ?: return

        // Çerezleri sıfırla
        CookieManager.getInstance().removeAllCookies(null)
        CookieManager.getInstance().flush()

        binding.webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
        }

        binding.webView.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView?, finishedUrl: String?) {
                super.onPageFinished(view, finishedUrl)

                if (finishedUrl != null && detectPlatform(finishedUrl) == platform) {
                    val cookieManager = CookieManager.getInstance()
                    val rawCookies = collectCookiesForPlatform(platform, cookieManager)
                    val requiredCookies = getRequiredCookiesForPlatform(platform)

                    val cookieMap = rawCookies.split(";").mapNotNull {
                        val parts = it.trim().split("=", limit = 2)
                        if (parts.size == 2) parts[0] to parts[1] else null
                    }.toMap()

                    val missing = requiredCookies.filter { it !in cookieMap }

                    if (missing.isEmpty()) {
                        getSharedPreferences("cookies", Context.MODE_PRIVATE)
                            .edit().putString("cookies_$platform", rawCookies).apply()

                        val resultIntent = Intent().apply {
                            putExtra("platform", platform)
                            putExtra("cookies", rawCookies)
                        }

                        setResult(RESULT_OK, resultIntent)
                        Toast.makeText(this@WebViewActivity, "$platform çerezleri alındı ✅", Toast.LENGTH_SHORT).show()
                        finish()
                    } else {
                        Toast.makeText(
                            this@WebViewActivity,
                            "Eksik çerez(ler): ${missing.joinToString(", ")}",
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
            url.contains("instagram.com") -> "instagram"
            url.contains("youtube.com") || url.contains("google.com") -> "youtube"
            url.contains("twitter.com") || url.contains("x.com") -> "twitter"
            else -> null
        }
    }

    private fun getRequiredCookiesForPlatform(platform: String): List<String> {
        return when (platform) {
            "instagram" -> listOf("sessionid", "ds_user_id", "csrftoken")
            "youtube" -> listOf("SID", "HSID", "SSID", "PREF", "YSC")
            "twitter" -> listOf("auth_token", "ct0", "twid")
            else -> emptyList()
        }
    }

    private fun collectCookiesForPlatform(platform: String, cookieManager: CookieManager): String {
        val domains = when (platform) {
            "youtube" -> listOf("https://www.youtube.com")
            "instagram" -> listOf("https://www.instagram.com")
            "twitter" -> listOf(
                "https://twitter.com",
                "https://www.twitter.com",
                "https://mobile.twitter.com",
                "https://x.com",
                "https://www.x.com"
            )
            else -> emptyList()
        }

        return domains
            .mapNotNull { cookieManager.getCookie(it) }
            .joinToString("; ")
            .split("; ")
            .distinct()
            .joinToString("; ")
    }
}
