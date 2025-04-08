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
import java.io.InputStream
import java.util.Locale


class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var folderPickerLauncher: androidx.activity.result.ActivityResultLauncher<Intent>
    private lateinit var webViewLauncher: androidx.activity.result.ActivityResultLauncher<Intent>

    companion object {
        private const val KEY_THEME_MODE = "theme_mode"
        private const val PREF_KEY_FOLDER_URI = "selected_folder_uri"
        private const val PREF_KEY_GALLERY_PERMISSION = "allow_gallery_save"
        private const val GALLERY_PREF_CHECKED_KEY = "gallery_pref_checked"
    }
    private lateinit var openFolderLauncher: androidx.activity.result.ActivityResultLauncher<Intent>
    private lateinit var downloadFolderLauncher: ActivityResultLauncher<Intent>
    // private lateinit var languageSpinner: Spinner

    override fun attachBaseContext(newBase: Context) {
        val updatedContext = LocaleHelper.applySavedLocale(newBase)
        super.attachBaseContext(updatedContext)
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        ThemeHelper.applySavedTheme(this)


        val savedLang = PrefsHelper.get(this, "selected_language", "tr")


//        languageSpinner = findViewById(R.id.languageSpinner)
//        LanguageHelper.setupLanguageSpinner(
//            this,
//            languageSpinner,
//            savedLang ?: "tr"
//        ) { newLang ->
//            setLocale(newLang)
//        }



        openFolderLauncher = registerForActivityResult(
            androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult()
        ) { result ->
            if (result.resultCode == RESULT_OK) {
                val folderUri = result.data?.data ?: return@registerForActivityResult
                contentResolver.takePersistableUriPermission(
                    folderUri,
                    Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                )
                PrefsHelper.save(this, "downloads_uri", folderUri.toString())
            }
        }

        downloadFolderLauncher = registerForActivityResult(
            ActivityResultContracts.StartActivityForResult()
        ) { result ->
            if (result.resultCode == RESULT_OK) {
                val folderUri = result.data?.data ?: return@registerForActivityResult
                contentResolver.takePersistableUriPermission(
                    folderUri,
                    Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                )
                ToastHelper.show(this, R.string.msg_download_folder_saved)
            }
        }

        // Launcher - WebView
        webViewLauncher = registerForActivityResult(
            androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult()
        ) { result ->
            if (result.resultCode == RESULT_OK) {
                val platform = result.data?.getStringExtra("platform") // gelen platform adı
                val cookies = result.data?.getStringExtra("cookies")
                if (!cookies.isNullOrEmpty() && !platform.isNullOrEmpty()) {
                    PrefsHelper.save(this, "cookies_$platform", cookies)
                    ToastHelper.show(this, R.string.msg_cookie_success, platform)
                } else {
                    ToastHelper.show(this, R.string.msg_cookie_fail)
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
                val currentMode = AppCompatDelegate.getDefaultNightMode()
                PrefsHelper.saveInt(this@MainActivity, KEY_THEME_MODE, currentMode)
                ToastHelper.show(this, R.string.msg_folder_selected)
            }
        }

        // Tema ayarları
        val themeMode = PrefsHelper.getInt(this, KEY_THEME_MODE, AppCompatDelegate.MODE_NIGHT_NO)
        AppCompatDelegate.setDefaultNightMode(themeMode)




        // UI bağlantıları
        setSupportActionBar(binding.topAppBar)
        setupSpinners()

        binding.buttonDownload.setOnClickListener {
            DownloadHandler.handleDownload(
                context = this,
                lifecycleScope = lifecycleScope,
                url = binding.editTextUrl.text.toString(),
                platform = SpinnerHelper.getPlatformCodeAt(binding.spinnerPlatform.selectedItemPosition),
                type = SpinnerHelper.getTypeCodeAt(binding.spinnerType.selectedItemPosition),
                fileNameInput = binding.editTextFileName.text.toString().trim(),
                progressBar = binding.progressBar,
                onSuccess = { file ->
                    ToastHelper.long(this, R.string.msg_saved_file, file.name)
                },
                onError = { message ->
                    ToastHelper.long(this, R.string.msg_api_error, message)
                },
                onClearInputs = {
                    binding.editTextUrl.text.clear()
                    binding.editTextFileName.text.clear()
                    binding.spinnerPlatform.setSelection(0)
                    binding.spinnerType.setSelection(0)
                }
            )
        }



        binding.buttonOpenDownload.setOnClickListener {
            FolderHelper.openOrSelectDownloadFolder(this, downloadFolderLauncher)
        }


        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    private fun saveFileWithPreferences(
        responseBody: ResponseBody,
        contentDisposition: String?,
        context: Context,
        type: String
    ): File? {
        val fileName = contentDisposition?.substringAfter("filename=")?.replace("\"", "")
            ?: "indirilen_dosya_${System.currentTimeMillis()}.tmp"

        return DownloadHelper.saveFileFromResponse(responseBody, fileName, context)
    }



    private fun openWebView(url: String) {
        val intent = Intent(this, WebViewActivity::class.java)
        intent.putExtra("url", url)
        webViewLauncher.launch(intent)
    }



    private fun setLocale(languageCode: String) {
        LocaleHelper.saveLocale(this, languageCode)
        restartActivity()
    }


    private fun restartActivity() {
        val intent = intent
        finish()
        startActivity(intent)
    }





    private fun saveToDownloadMateFolder(
        responseBody: ResponseBody,
        fileName: String,
        context: Context
    ): File? {
        val lang = getSharedPreferences("app_preferences", MODE_PRIVATE)
            .getString("selected_language", "tr") ?: "tr"
        return DownloadHelper.saveToDownloadMateFolder(responseBody, fileName, context, lang)
    }





    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.toolbar_menu, menu)
//        val toggleItem = menu?.findItem(R.id.action_toggle_theme)
//        val switch = toggleItem?.actionView as? SwitchCompat
//        val isDark = isNightMode()
//        switch?.isChecked = isDark
//        val thumbColor = if (isDark) Color.WHITE else Color.BLACK
//        val trackColor = if (isDark) Color.LTGRAY else Color.DKGRAY
//        switch?.apply {
//            setBackgroundColor(Color.TRANSPARENT)
//            thumbDrawable?.setTint(thumbColor)
//            trackDrawable?.setTint(trackColor)
//            setOnCheckedChangeListener { _, isChecked ->
//                val mode = if (isChecked) AppCompatDelegate.MODE_NIGHT_YES else AppCompatDelegate.MODE_NIGHT_NO
//                AppCompatDelegate.setDefaultNightMode(mode)
//                PrefsHelper.saveInt(this@MainActivity, KEY_THEME_MODE, mode)
//                setSocialIconsForTheme()
//            }
//        }
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_settings -> {
                val intent = Intent(this, SettingsActivity::class.java)
                startActivity(intent)
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    private fun isNightMode(): Boolean {
        val currentNightMode = resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK
        return currentNightMode == Configuration.UI_MODE_NIGHT_YES
    }



    private fun setupSpinners() {
        SpinnerHelper.setupPlatformAndTypeSpinners(
            this,
            binding.spinnerPlatform,
            binding.spinnerType,
            isNightMode(),
        ) { bgColor, textColor ->
            binding.buttonDownload.setBackgroundColor(bgColor)
            textColor?.let { binding.buttonDownload.setTextColor(it) }
        }
    }

}
