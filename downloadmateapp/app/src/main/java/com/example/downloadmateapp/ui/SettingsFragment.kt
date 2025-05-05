package com.example.downloadmateapp.ui

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageButton
import android.widget.Spinner
import android.widget.TextView
import androidx.appcompat.app.AppCompatDelegate
import androidx.appcompat.widget.SwitchCompat
import androidx.fragment.app.Fragment
import com.example.downloadmateapp.R
import com.example.downloadmateapp.helper.LanguageHelper
import com.example.downloadmateapp.helper.LocaleHelper
import com.example.downloadmateapp.helper.PrefsHelper
import com.example.downloadmateapp.helper.SocialHelper
import com.example.downloadmateapp.helper.ThemeHelper
import com.example.downloadmateapp.helper.ToastHelper

class SettingsFragment : Fragment() {

    private lateinit var languageSpinner: Spinner
    private lateinit var switchTheme: SwitchCompat
    private lateinit var buttonInstagram: ImageButton
    private lateinit var buttonYouTube: ImageButton
    private lateinit var buttonTwitter: ImageButton
    private lateinit var buttonSelectFolder: Button
    private lateinit var textSelectedPath: TextView

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_settings, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        languageSpinner = view.findViewById(R.id.languageSpinner)
        switchTheme = view.findViewById(R.id.switchTheme)
        buttonInstagram = view.findViewById(R.id.buttonInstagram)
        buttonYouTube = view.findViewById(R.id.buttonYouTube)
        buttonTwitter = view.findViewById(R.id.buttonTwitter)
        buttonSelectFolder = view.findViewById(R.id.buttonSelectFolder)
        textSelectedPath = view.findViewById(R.id.textSelectedPath)

        val selectedLang = PrefsHelper.get(requireContext(), "selected_language", "tr") ?: "tr"
        LanguageHelper.setupLanguageSpinner(
            requireContext(), languageSpinner, selectedLang
        ) { newLang ->
            LocaleHelper.saveLocale(requireContext(), newLang)

            requireActivity().recreate()
        }

        val currentMode = PrefsHelper.getInt(requireContext(), "theme_mode", AppCompatDelegate.MODE_NIGHT_NO)
        switchTheme.isChecked = (currentMode == AppCompatDelegate.MODE_NIGHT_YES)
        switchTheme.setOnCheckedChangeListener { _, isChecked ->
            val newMode = if (isChecked) AppCompatDelegate.MODE_NIGHT_YES else AppCompatDelegate.MODE_NIGHT_NO
            AppCompatDelegate.setDefaultNightMode(newMode)
            PrefsHelper.saveInt(requireContext(), "theme_mode", newMode)
            ThemeHelper.applySavedTheme(requireContext())
        }

        val buttons = mapOf(
            buttonInstagram to "https://www.instagram.com/accounts/login/",
            buttonYouTube to "https://www.youtube.com/feed/subscriptions",
            buttonTwitter to "https://twitter.com/i/flow/login"
        )
        SocialHelper.setupSocialButtons(requireActivity(), buttons)
        SocialHelper.setIconsForTheme(requireActivity(), buttonInstagram, buttonYouTube, buttonTwitter)

        textSelectedPath.text = getString(R.string.text_selected_path)

        buttonSelectFolder.setOnClickListener {
            try {
                val intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)
                startActivity(intent)
            } catch (e: Exception) {
                ToastHelper.show(requireContext(), R.string.toast_cannot_open_folder)
            }
        }
    }
}
