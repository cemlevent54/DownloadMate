package com.example.downloadmateapp

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.os.PersistableBundle
import android.view.MenuItem
import android.widget.Spinner
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.appcompat.widget.SwitchCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.setPadding
import com.example.downloadmateapp.helper.LanguageHelper
import com.example.downloadmateapp.helper.LocaleHelper
import com.example.downloadmateapp.helper.PrefsHelper
import com.example.downloadmateapp.helper.ThemeHelper
import com.google.android.material.appbar.MaterialToolbar
import java.util.Locale

class SettingsActivity: AppCompatActivity() {
    private lateinit var languageSpinner: Spinner
    private lateinit var switchTheme: SwitchCompat

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
    }


    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            android.R.id.home -> {
                onBackPressedDispatcher.onBackPressed() // Geri tuşuna bastırmak
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