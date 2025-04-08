package com.example.downloadmateapp

import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.net.Uri
import android.os.Bundle
import android.provider.DocumentsContract
import android.view.MenuItem
import android.widget.Button
import android.widget.ImageButton
import android.widget.Spinner
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.appcompat.widget.SwitchCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.setPadding
import com.example.downloadmateapp.helper.*
import com.google.android.material.appbar.MaterialToolbar

class SettingsActivity : AppCompatActivity() {
    private lateinit var languageSpinner: Spinner
    private lateinit var switchTheme: SwitchCompat
    private lateinit var buttonInstagram: ImageButton
    private lateinit var buttonYouTube: ImageButton
    private lateinit var buttonTwitter: ImageButton
    private lateinit var buttonSelectFolder: Button
    private lateinit var textSelectedPath: TextView
    private lateinit var folderPickerLauncher: ActivityResultLauncher<Intent>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_settings)

        val rootLayout = findViewById<androidx.constraintlayout.widget.ConstraintLayout>(R.id.rootLayout)
        ViewCompat.setOnApplyWindowInsetsListener(rootLayout) { view, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            view.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val toolbar = findViewById<MaterialToolbar>(R.id.toolbar)
        setSupportActionBar(toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        // UI bağlantıları
        languageSpinner = findViewById(R.id.languageSpinner)
        switchTheme = findViewById(R.id.switchTheme)

        buttonInstagram = findViewById(R.id.buttonInstagram)
        buttonYouTube = findViewById(R.id.buttonYouTube)
        buttonTwitter = findViewById(R.id.buttonTwitter)

        val selectedLang = PrefsHelper.get(this, "selected_language", "tr") ?: "tr"
        LanguageHelper.setupLanguageSpinner(
            context = this,
            spinner = languageSpinner,
            savedLang = selectedLang
        ) { newLang ->
            LocaleHelper.saveLocale(this, newLang)
            val intent = Intent(this, MainActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP or
                    Intent.FLAG_ACTIVITY_NEW_TASK or
                    Intent.FLAG_ACTIVITY_CLEAR_TASK
            startActivity(intent)
            finish()
        }

        val currentMode = PrefsHelper.getInt(this, "theme_mode", AppCompatDelegate.MODE_NIGHT_NO)
        switchTheme.isChecked = (currentMode == AppCompatDelegate.MODE_NIGHT_YES)

        switchTheme.setOnCheckedChangeListener { _, isChecked ->
            val newMode = if (isChecked) {
                AppCompatDelegate.MODE_NIGHT_YES
            } else {
                AppCompatDelegate.MODE_NIGHT_NO
            }

            AppCompatDelegate.setDefaultNightMode(newMode)
            PrefsHelper.saveInt(this, "theme_mode", newMode)
            ThemeHelper.applySavedTheme(this)
        }

        // Sosyal medya butonlarını ve ikonlarını ayarla
        val buttons = mapOf(
            buttonInstagram to "https://www.instagram.com/accounts/login/",
            buttonYouTube to "https://www.youtube.com/feed/subscriptions",
            buttonTwitter to "https://twitter.com/i/flow/login"
        )
        SocialHelper.setupSocialButtons(this, buttons)
        SocialHelper.setIconsForTheme(this, buttonInstagram, buttonYouTube, buttonTwitter)

        buttonSelectFolder = findViewById(R.id.buttonSelectFolder)
        textSelectedPath = findViewById(R.id.textSelectedPath)

        textSelectedPath.text = getString(R.string.text_selected_path)

        buttonSelectFolder.setOnClickListener {
            try {
                val intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE).apply {
                    putExtra(
                        DocumentsContract.EXTRA_INITIAL_URI,
                        Uri.parse("content://com.android.externalstorage.documents/document/primary%3ADownload%2FDownloadMateDownloads"))
                }
                startActivity(intent)
            } catch (e: Exception) {
                ToastHelper.show(this, R.string.toast_cannot_open_folder)
            }
        }





    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            android.R.id.home -> {
                onBackPressedDispatcher.onBackPressed()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    override fun attachBaseContext(newBase: Context) {
        val updatedContext = LocaleHelper.applySavedLocale(newBase)
        super.attachBaseContext(updatedContext)
    }
}