package com.example.downloadmateapp.adapter

import android.content.Intent
import android.net.Uri
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.core.content.FileProvider
import androidx.documentfile.provider.DocumentFile
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.downloadmateapp.R
import com.example.downloadmateapp.helper.ToastHelper
import java.io.File
import java.util.Locale

class DownloadedFileAdapter : ListAdapter<File, DownloadedFileAdapter.FileViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): FileViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_downloaded_file, parent, false)
        return FileViewHolder(view)
    }

    override fun onBindViewHolder(holder: FileViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class FileViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val fileNameText: TextView = itemView.findViewById(R.id.textFileName)
        private val buttonPlay: ImageButton = itemView.findViewById(R.id.buttonPlay)

        fun bind(file: File) {
            fileNameText.text = file.name

            buttonPlay.setOnClickListener {
                val context = itemView.context
                val downloadsFolderUri = Uri.parse("content://com.android.externalstorage.documents/document/primary:Download/DownloadMateDownloads")

                val intent = Intent(Intent.ACTION_VIEW).apply {
                    setDataAndType(downloadsFolderUri, "resource/folder")
                    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                }

                // SAF ile dosya yöneticisini aç
                val openIntent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE).apply {
                    putExtra("android.provider.extra.INITIAL_URI", downloadsFolderUri)
                }

                context.startActivity(openIntent)
            }


        }


        private fun getMimeType(file: File): String {
            return when (file.extension.lowercase(Locale.getDefault())) {
                "mp4" -> "video/mp4"
                "mp3" -> "audio/mpeg"
                else -> "*/*"
            }
        }
    }

    class DiffCallback : DiffUtil.ItemCallback<File>() {
        override fun areItemsTheSame(oldItem: File, newItem: File) = oldItem.path == newItem.path
        override fun areContentsTheSame(oldItem: File, newItem: File) = oldItem == newItem
    }
}
