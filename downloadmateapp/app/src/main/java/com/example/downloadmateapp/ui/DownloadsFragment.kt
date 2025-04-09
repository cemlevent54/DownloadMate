package com.example.downloadmateapp.ui

import android.content.Intent
import android.os.Bundle
import android.view.*
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.MenuHost
import androidx.core.view.MenuProvider
import androidx.fragment.app.Fragment
import androidx.lifecycle.Lifecycle
import com.example.downloadmateapp.R
import com.example.downloadmateapp.SettingsActivity
import com.example.downloadmateapp.databinding.FragmentDownloadsBinding
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.downloadmateapp.adapter.DownloadedFileAdapter
import java.io.File

class DownloadsFragment : Fragment() {

    private var _binding: FragmentDownloadsBinding? = null
    private val binding get() = _binding!!

    private lateinit var adapter: DownloadedFileAdapter

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentDownloadsBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        (requireActivity() as AppCompatActivity).setSupportActionBar(binding.topAppBar)

        ViewCompat.setOnApplyWindowInsetsListener(binding.rootLayout) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        setupMenu()
        setupDownloadsList()
    }

    private fun setupMenu() {
        val menuHost: MenuHost = requireActivity()
        menuHost.addMenuProvider(object : MenuProvider {
            override fun onCreateMenu(menu: Menu, menuInflater: MenuInflater) {
                menuInflater.inflate(R.menu.top_app_bar_menu, menu)
            }

            override fun onMenuItemSelected(menuItem: MenuItem): Boolean {
                return when (menuItem.itemId) {
                    R.id.action_settings -> {
                        startActivity(Intent(requireContext(), SettingsActivity::class.java))
                        true
                    }
                    else -> false
                }
            }
        }, viewLifecycleOwner, Lifecycle.State.RESUMED)
    }

    private fun setupDownloadsList() {
        adapter = DownloadedFileAdapter()
        binding.recyclerDownloads.layoutManager = LinearLayoutManager(requireContext())
        binding.recyclerDownloads.adapter = adapter

        val publicDownloads = android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS)
        val downloadFolder = File(publicDownloads, "DownloadMateDownloads")

        if (!downloadFolder.exists()) {
            downloadFolder.mkdirs()
        }

        val files = downloadFolder.listFiles { file ->
            file.extension.equals("mp4", ignoreCase = true) || file.extension.equals("mp3", ignoreCase = true)
        }?.sortedByDescending { it.lastModified() } ?: emptyList()

        if (files.isNotEmpty()) {
            binding.emptyText.visibility = View.GONE
            binding.recyclerDownloads.visibility = View.VISIBLE
            adapter.submitList(files)
        } else {
            binding.emptyText.visibility = View.VISIBLE
            binding.recyclerDownloads.visibility = View.GONE
        }
    }


    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}