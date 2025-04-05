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
import java.io.InputStream
import java.util.Locale


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
    private lateinit var openFolderLauncher: androidx.activity.result.ActivityResultLauncher<Intent>
    private lateinit var downloadFolderLauncher: ActivityResultLauncher<Intent>
    private lateinit var languageSpinner: Spinner



    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // 1. Dili uygula
        val savedLang = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
            .getString("selected_language", null)

        if (savedLang != null) {
            val locale = Locale(savedLang)
            Locale.setDefault(locale)
            val config = resources.configuration
            config.setLocale(locale)
            baseContext.resources.updateConfiguration(config, baseContext.resources.displayMetrics)
        }

        // 2. Spinner'ı bağla
        languageSpinner = findViewById(R.id.languageSpinner)
        val languages = listOf("Türkçe", "English")
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, languages)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        languageSpinner.adapter = adapter

        // 3. Kaydedilen dile göre spinner pozisyonunu ayarla
        val initialPos = if (savedLang == "en") 1 else 0
        languageSpinner.setSelection(initialPos)

        // 4. Seçime göre dili değiştir
        languageSpinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>, view: View?, position: Int, id: Long) {
                val selectedLanguage = when (position) {
                    0 -> "tr"
                    1 -> "en"
                    else -> "tr"
                }
                if (selectedLanguage != savedLang) {
                    setLocale(selectedLanguage)
                }
            }

            override fun onNothingSelected(parent: AdapterView<*>) {}
        }


        openFolderLauncher = registerForActivityResult(
            androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult()
        ) { result ->
            if (result.resultCode == RESULT_OK) {
                val folderUri = result.data?.data ?: return@registerForActivityResult
                contentResolver.takePersistableUriPermission(
                    folderUri,
                    Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                )
                getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
                    .edit()
                    .putString("downloads_uri", folderUri.toString())
                    .apply()
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
                getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
                    .edit()
                    .putString("downloads_uri", folderUri.toString())
                    .apply()
                showToast(R.string.msg_download_folder_saved)
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
                    getSharedPreferences("cookies", Context.MODE_PRIVATE)
                        .edit()
                        .putString("cookies_$platform", cookies)
                        .apply()
                    showToast(R.string.msg_cookie_success, platform)
                } else {
                    showToast(R.string.msg_cookie_fail)
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
                showToast(R.string.msg_folder_selected)
            }
        }

        // Tema ayarları
        val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        AppCompatDelegate.setDefaultNightMode(
            prefs.getInt(KEY_THEME_MODE, AppCompatDelegate.MODE_NIGHT_NO)
        )




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
                Toast.makeText(this, getString(R.string.msg_fill_all_fields), Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            binding.progressBar.visibility = View.VISIBLE
            val request = DownloadRequest(url = url, type = type)

            lifecycleScope.launch {
                try {
                    val cookies = getSharedPreferences("cookies", Context.MODE_PRIVATE)
                        .getString("cookies_$platform", null)

                    if (cookies.isNullOrEmpty()) {
                        Toast.makeText(this@MainActivity, getString(R.string.msg_cookie_missing, platform), Toast.LENGTH_LONG).show()
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

                                Toast.makeText(
                                    this@MainActivity,
                                    getString(R.string.msg_saved_file, finalFile.name),
                                    Toast.LENGTH_LONG
                                ).show()
                            }
                        }

                        // 🎯 Alanları temizle
                        binding.editTextUrl.text.clear()
                        binding.editTextFileName.text.clear()
                        binding.spinnerPlatform.setSelection(0)
                        binding.spinnerType.setSelection(0)

                    } else {
                        val msg = response?.errorBody()?.string() ?: "Bilinmeyen hata"
                        Toast.makeText(this@MainActivity, getString(R.string.msg_api_error, msg), Toast.LENGTH_LONG).show()
                    }

                } catch (e: Exception) {
                    Toast.makeText(this@MainActivity, getString(R.string.msg_general_error, e.message), Toast.LENGTH_SHORT).show()
                } finally {
                    binding.progressBar.visibility = View.GONE
                }
            }
        }



        binding.buttonOpenDownload.setOnClickListener {
            val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
            val uriStr = prefs.getString("downloads_uri", null)

            if (uriStr != null) {
                try {
                    val treeUri = Uri.parse(uriStr)
                    val docUri = DocumentsContract.buildDocumentUriUsingTree(
                        treeUri,
                        DocumentsContract.getTreeDocumentId(treeUri)
                    )

                    val intent = Intent(Intent.ACTION_VIEW).apply {
                        setDataAndType(docUri, DocumentsContract.Document.MIME_TYPE_DIR)
                        addFlags(
                            Intent.FLAG_GRANT_READ_URI_PERMISSION or
                                    Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                        )
                    }

                    startActivity(intent)

                } catch (e: Exception) {
                    e.printStackTrace()
                    Toast.makeText(this, getString(R.string.msg_folder_open_error, e.message), Toast.LENGTH_LONG).show()
                }
            } else {
                showToast(R.string.msg_select_download_folder)

                val intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE).apply {
                    addFlags(
                        Intent.FLAG_GRANT_READ_URI_PERMISSION or
                                Intent.FLAG_GRANT_WRITE_URI_PERMISSION or
                                Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
                    )
                }
                downloadFolderLauncher.launch(intent)
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

    private fun showToast(resId: Int, vararg formatArgs: Any?) {
        Toast.makeText(this, getString(resId, *formatArgs), Toast.LENGTH_SHORT).show()
    }

    private fun setLocale(languageCode: String) {
        val locale = Locale(languageCode)
        Locale.setDefault(locale)
        val config = resources.configuration
        config.setLocale(locale)
        baseContext.resources.updateConfiguration(config, baseContext.resources.displayMetrics)

        // Tercihi kaydet
        getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
            .edit()
            .putString("selected_language", languageCode)
            .apply()

        // Aktiviteyi yeniden başlat
        restartActivity() // recreate() yerine
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
        return try {
            val downloadsDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
            val appFolder = File(downloadsDir, "DownloadMateDownloads")
            if (!appFolder.exists()) appFolder.mkdirs()

            val file = File(appFolder, fileName)
            val inputStream = responseBody.byteStream()
            val outputStream = FileOutputStream(file)
            inputStream.use { it.copyTo(outputStream) }

            val currentLang = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
                .getString("selected_language", "tr")
            val msg = if (currentLang == "tr") {
                "✅ Dosya kaydedildi: ${file.absolutePath}"
            } else {
                "✅ File saved: ${file.absolutePath}"
            }
            Toast.makeText(context, msg, Toast.LENGTH_SHORT).show()
            android.util.Log.d("DownloadMate", msg)

            file
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(this, getString(R.string.msg_folder_open_error, e.message), Toast.LENGTH_LONG).show()
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
        val platforms = listOf(
            getString(R.string.select_option),
            getString(R.string.platform_youtube),
            getString(R.string.platform_instagram),
            getString(R.string.platform_twitter)
        )

        val types = listOf(
            getString(R.string.select_option),
            getString(R.string.type_video),
            getString(R.string.type_audio)
        )

        binding.spinnerPlatform.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, platforms)
            .also { it.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item) }

        binding.spinnerType.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, types)
            .also { it.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item) }

        binding.spinnerPlatform.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>, view: View?, pos: Int, id: Long) {
                val selected = parent.getItemAtPosition(pos).toString().lowercase()
                when (selected) {
                    getString(R.string.platform_youtube).lowercase() -> binding.buttonDownload.setBackgroundColor(Color.parseColor("#FF0000"))
                    getString(R.string.platform_twitter).lowercase() -> binding.buttonDownload.setBackgroundColor(Color.parseColor("#1DA1F2"))
                    getString(R.string.platform_instagram).lowercase() -> binding.buttonDownload.setBackgroundColor(Color.parseColor("#c13584"))
                    getString(R.string.select_option).lowercase() -> {
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
