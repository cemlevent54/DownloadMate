package com.example.downloadmateapp

import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.provider.DocumentsContract
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Spinner
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
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
import androidx.core.content.FileProvider
import androidx.core.view.WindowCompat
import com.example.downloadmateapp.helper.DownloadHandler
import com.example.downloadmateapp.helper.DownloadHelper
import com.example.downloadmateapp.helper.FolderHelper
import com.example.downloadmateapp.helper.LanguageHelper
import com.example.downloadmateapp.helper.LocaleHelper
import com.example.downloadmateapp.helper.PrefsHelper
import com.example.downloadmateapp.helper.SocialHelper
import com.example.downloadmateapp.helper.SpinnerHelper
import com.example.downloadmateapp.helper.ThemeHelper
import com.example.downloadmateapp.helper.ToastHelper
import com.example.downloadmateapp.ui.DownloadsFragment
import com.example.downloadmateapp.ui.HomeFragment
import com.google.android.material.bottomnavigation.BottomNavigationView
import java.io.InputStream
import java.util.Locale


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        ThemeHelper.applySavedTheme(this)
        WindowCompat.setDecorFitsSystemWindows(window, true)

        // Varsayılan olarak HomeFragment göster
        if (savedInstanceState == null) {
            supportFragmentManager.beginTransaction()
                .replace(R.id.fragmentContainer, HomeFragment())
                .commit()
        }

        val bottomNav = findViewById<BottomNavigationView>(R.id.bottomNavigation)
        bottomNav.setOnItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_home -> {
                    supportFragmentManager.beginTransaction()
                        .replace(R.id.fragmentContainer, HomeFragment())
                        .commit()
                    true
                }
                R.id.nav_downloads -> {
                    supportFragmentManager.beginTransaction()
                        .replace(R.id.fragmentContainer, DownloadsFragment())
                        .commit()
                    true
                }
                else -> false
            }
        }
    }

    override fun attachBaseContext(newBase: Context) {
        val updatedContext = LocaleHelper.applySavedLocale(newBase)
        super.attachBaseContext(updatedContext)
    }
}

