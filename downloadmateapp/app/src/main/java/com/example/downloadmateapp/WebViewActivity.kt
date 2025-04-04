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

        binding.webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
        }

        binding.webView.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView?, finishedUrl: String?) {
                super.onPageFinished(view, finishedUrl)

                finishedUrl?.let {
                    val cookieManager = CookieManager.getInstance()
                    val cookies = cookieManager.getCookie(it)

                    if (!cookies.isNullOrBlank()) {
                        val resultIntent = Intent().apply {
                            putExtra("cookies", cookies)
                        }

                        setResult(RESULT_OK, resultIntent)
                        Toast.makeText(
                            this@WebViewActivity,
                            "Çerezler başarıyla alındı ✅",
                            Toast.LENGTH_SHORT
                        ).show()

                        finish() // Geri dön
                    }
                }
            }
        }

        binding.webView.loadUrl(url)
    }
}
