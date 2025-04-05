package com.example.downloadmateapp.helper

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.DocumentsContract
import androidx.activity.result.ActivityResultLauncher
import com.example.downloadmateapp.R

object FolderHelper {

    fun openOrSelectDownloadFolder(
        context: Context,
        downloadFolderLauncher: ActivityResultLauncher<Intent>
    ) {
        val uriStr = PrefsHelper.get(context, "downloads_uri")

        if (uriStr.isNotBlank()) {
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

                context.startActivity(intent)

            } catch (e: Exception) {
                e.printStackTrace()
                ToastHelper.long(context, R.string.msg_folder_open_error, e.message)
            }
        } else {
            ToastHelper.show(context, R.string.msg_select_download_folder)

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
}