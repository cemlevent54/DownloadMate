package com.example.downloadmateapp

import android.content.Context
import android.content.res.Configuration
import android.graphics.Color
import android.os.Bundle
import android.os.Environment
import android.view.Menu
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
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
import java.io.InputStream

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    // SharedPreferences
    companion object {
        private const val PREFS_NAME = "app_preferences"
        private const val KEY_THEME_MODE = "theme_mode"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        // SharedPreferences ekleme
        val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        val savedMode = prefs.getInt(KEY_THEME_MODE, AppCompatDelegate.MODE_NIGHT_NO)
        AppCompatDelegate.setDefaultNightMode(savedMode)

        setContentView(R.layout.activity_main)

        // Set up the view binding
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Toolbar menü tanımlanıyor
        setSupportActionBar(binding.topAppBar)

        // Spinner verilerini ata
        setupSpinners()

        // Butona tıklama işlemi
        binding.buttonDownload.setOnClickListener {
            val url = binding.editTextUrl.text.toString()
            val platform = binding.spinnerPlatform.selectedItem.toString().lowercase()
            val type = binding.spinnerType.selectedItem.toString().lowercase()

            if (platform == "seçiniz" || type == "seçiniz" || url.isBlank()) {
                Toast.makeText(this, "Lütfen tüm alanları doldurun", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            binding.progressBar.visibility = View.VISIBLE

            val request = DownloadRequest(url = url, type = type)

            lifecycleScope.launch {
                try {
                    val response = when (platform) {
                        "youtube" -> RetrofitClient.apiService.downloadYoutube(request)
                        "instagram" -> RetrofitClient.apiService.downloadInstagram(request)
                        "twitter" -> RetrofitClient.apiService.downloadTwitter(request)
                        else -> null
                    }

                    if (response != null) {
                        if (response.isSuccessful) {
                            val contentDisposition = response.headers()["Content-Disposition"]
                            response.body()?.let { body ->
                                val savedFile = saveToDownloadMateFolder(body, contentDisposition, this@MainActivity)
                                if (savedFile != null) {
                                    Toast.makeText(this@MainActivity, "Kaydedildi: ${savedFile.name}", Toast.LENGTH_LONG).show()
                                }
                            }
                        } else {
                            // ❗ API 500, 400 gibi başarısız cevap verdiğinde
                            val errorMsg = response.errorBody()?.string() ?: "Bilinmeyen hata oluştu."
                            Toast.makeText(this@MainActivity, "API Hatası: $errorMsg", Toast.LENGTH_LONG).show()
                        }
                    } else {
                        Toast.makeText(this@MainActivity, "Sunucudan yanıt alınamadı", Toast.LENGTH_LONG).show()
                    }


                } catch (e: Exception) {
                    Toast.makeText(this@MainActivity, "Hata: ${e.message}", Toast.LENGTH_SHORT).show()
                } finally {
                    binding.progressBar.visibility = View.GONE
                }
            }
        }



        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    private fun writeResponseBodyToDisk(body: ResponseBody, file: File) {
        try {
            val input: InputStream = body.byteStream()
            val output = FileOutputStream(file)

            input.use { inputStream ->
                output.use { fileOut ->
                    inputStream.copyTo(fileOut)
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun saveToDownloadMateFolder(
        responseBody: ResponseBody,
        contentDisposition: String?,
        context: Context
    ): File? {
        try {
            // 🔍 Dosya adını Content-Disposition header'ından çek
            val fileName = contentDisposition
                ?.substringAfter("filename=")
                ?.replace("\"", "")
                ?: "indirilen_dosya_${System.currentTimeMillis()}.tmp"

            val downloadsDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
            val appFolder = File(downloadsDir, "DownloadMateDownloads")
            if (!appFolder.exists()) {
                val created = appFolder.mkdirs()
                if (!created) {
                    Toast.makeText(context, "Klasör oluşturulamadı", Toast.LENGTH_SHORT).show()
                    return null
                }
            }

            val file = File(appFolder, fileName)
            val inputStream = responseBody.byteStream()
            val outputStream = FileOutputStream(file)

            inputStream.use { input ->
                outputStream.use { output ->
                    input.copyTo(output)
                }
            }

            return file

        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(context, "Dosya kaydedilirken hata oluştu", Toast.LENGTH_SHORT).show()
            return null
        }
    }



    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.toolbar_menu, menu)

        val toggleItem = menu?.findItem(R.id.action_toggle_theme)
        val switch = toggleItem?.actionView as? SwitchCompat

        val isDark = isNightMode()
        switch?.isChecked = isDark

        // 🌈 Renkleri moda göre belirle
        val thumbColor = if (isDark) android.graphics.Color.WHITE else android.graphics.Color.BLACK
        val trackColor = if (isDark) android.graphics.Color.LTGRAY else android.graphics.Color.DKGRAY

        switch?.apply {
            setBackgroundColor(android.graphics.Color.TRANSPARENT)

            thumbDrawable?.setTint(thumbColor)
            trackDrawable?.setTint(trackColor)

            setOnCheckedChangeListener { _, isChecked ->
                val mode = if (isChecked) {
                    AppCompatDelegate.MODE_NIGHT_YES
                } else {
                    AppCompatDelegate.MODE_NIGHT_NO
                }

                // Temayı uygula
                AppCompatDelegate.setDefaultNightMode(mode)

                // Tercihi kaydet
                getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
                    .edit()
                    .putInt(KEY_THEME_MODE, mode)
                    .apply()
            }


        }

        return true
    }

    private fun isNightMode(): Boolean {
        val currentNightMode = resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK
        return currentNightMode == Configuration.UI_MODE_NIGHT_YES
    }



    private fun setupSpinners() {
        // Platform Spinner
        val platforms = listOf("Seçiniz", "YouTube", "Instagram", "Twitter")
        val platformAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, platforms)
        platformAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        binding.spinnerPlatform.adapter = platformAdapter

        // Tür Spinner
        val types = listOf("Seçiniz", "Video", "Audio")
        val typeAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, types)
        typeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        binding.spinnerType.adapter = typeAdapter

        binding.spinnerPlatform.setOnItemSelectedListener(object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>, view: View?, position: Int, id: Long) {
                val selectedPlatform = parent.getItemAtPosition(position).toString().lowercase()

                when (selectedPlatform) {
                    "youtube" -> binding.buttonDownload.setBackgroundColor(Color.parseColor("#FF0000"))
                    "twitter", "x" -> binding.buttonDownload.setBackgroundColor(Color.parseColor("#1DA1F2"))
                    "instagram" -> binding.buttonDownload.setBackgroundColor(Color.parseColor("#c13584"))
                    "seçiniz" -> {
                        // Varsayılan tema renkleriyle bırak (örneğin siyah beyaz)
                        val isDark = isNightMode()
                        val defaultColor = if (isDark) Color.WHITE else Color.BLACK
                        val textColor = if (isDark) Color.BLACK else Color.WHITE

                        binding.buttonDownload.setBackgroundColor(defaultColor)
                        binding.buttonDownload.setTextColor(textColor)
                    }
                }

            }

            override fun onNothingSelected(parent: AdapterView<*>) {}
        })
    }
}