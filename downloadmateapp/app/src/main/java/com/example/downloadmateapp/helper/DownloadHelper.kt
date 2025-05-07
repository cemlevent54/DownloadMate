package com.example.downloadmateapp.helper

import android.content.Context
import android.os.Environment
import android.os.Handler
import android.os.Looper
import android.widget.Toast
import com.example.downloadmateapp.R
import okhttp3.ResponseBody
import java.io.File
import java.io.FileOutputStream

object DownloadHelper {

    fun saveToDownloadMateFolder(
        responseBody: ResponseBody,
        fileName: String,
        context: Context,
        language: String
    ): File? {
        return try {
            val downloadsDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
            val appFolder = File(downloadsDir, "DownloadMateDownloads")
            if (!appFolder.exists()) appFolder.mkdirs()

            val file = File(appFolder, fileName)
            responseBody.byteStream().use { input ->
                FileOutputStream(file).use { output ->
                    input.copyTo(output)
                }
            }

            val msg = if (language == "tr") {
                "✅ Dosya kaydedildi: ${file.absolutePath}"
            } else {
                "✅ File saved: ${file.absolutePath}"
            }
            // ⚠️ UI işlemi ana thread’e post ediliyor
            Handler(Looper.getMainLooper()).post {
                Toast.makeText(context, msg, Toast.LENGTH_SHORT).show()
            }
            android.util.Log.d("DownloadMate", msg)

            file
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(context, context.getString(R.string.msg_folder_open_error, e.message), Toast.LENGTH_LONG).show()
            null
        }
    }

    fun renameIfNeeded(file: File, newName: String?): File {
        if (!newName.isNullOrBlank() && newName.length <= 40) {
            val safeName = newName.replace(Regex("[^a-zA-Z0-9._-]"), "_")
            val renamed = File(file.parent, "$safeName.${file.extension}")
            file.renameTo(renamed)
            return renamed
        }
        return file
    }

    fun saveFileFromResponse(
        responseBody: ResponseBody,
        fileName: String,
        context: Context
    ): File? {
        val lang = PrefsHelper.get(context, "selected_language", "tr")
        return saveToDownloadMateFolder(responseBody, fileName, context, lang)
    }
}