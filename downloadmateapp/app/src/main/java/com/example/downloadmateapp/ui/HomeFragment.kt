package com.example.downloadmateapp.ui

import android.content.Intent
import android.os.Bundle
import android.view.*
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.example.downloadmateapp.R
import com.example.downloadmateapp.SettingsActivity
import com.example.downloadmateapp.databinding.FragmentHomeBinding
import com.example.downloadmateapp.helper.*

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!

    private val downloadFolderLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == android.app.Activity.RESULT_OK) {
                val folderUri = result.data?.data ?: return@registerForActivityResult
                requireContext().contentResolver.takePersistableUriPermission(
                    folderUri,
                    Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                )
                ToastHelper.show(requireContext(), R.string.msg_download_folder_saved)
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setHasOptionsMenu(true) // Ayarlar butonunu göstermek için gerekli
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        (requireActivity() as AppCompatActivity).setSupportActionBar(binding.topAppBar)
        (requireActivity() as AppCompatActivity).supportActionBar?.title = getString(R.string.app_name)

        ViewCompat.setOnApplyWindowInsetsListener(binding.rootLayout) { view, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            view.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        SpinnerHelper.setupPlatformAndTypeSpinners(
            requireContext(),
            binding.spinnerPlatform,
            binding.spinnerType,
            ThemeHelper.isNightMode(requireContext())
        ) { bgColor, textColor ->
            binding.buttonDownload.setBackgroundColor(bgColor)
            textColor?.let { binding.buttonDownload.setTextColor(it) }
        }

        binding.buttonDownload.setOnClickListener {
            DownloadHandler.handleDownload(
                context = requireContext(),
                lifecycleScope = viewLifecycleOwner.lifecycleScope,
                url = binding.editTextUrl.text.toString(),
                platform = SpinnerHelper.getPlatformCodeAt(binding.spinnerPlatform.selectedItemPosition),
                type = SpinnerHelper.getTypeCodeAt(binding.spinnerType.selectedItemPosition),
                fileNameInput = binding.editTextFileName.text.toString().trim(),
                progressBar = binding.progressBar,
                onSuccess = { file ->
                    ToastHelper.long(requireContext(), R.string.msg_saved_file, file.name)
                },
                onError = { message ->
                    ToastHelper.long(requireContext(), R.string.msg_api_error, message)
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
            FolderHelper.openOrSelectDownloadFolder(requireActivity(), downloadFolderLauncher)
        }
    }

    override fun onCreateOptionsMenu(menu: Menu, inflater: MenuInflater) {
        inflater.inflate(R.menu.top_app_bar_menu, menu)
        super.onCreateOptionsMenu(menu, inflater)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_settings -> {
                startActivity(Intent(requireContext(), SettingsActivity::class.java))
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
