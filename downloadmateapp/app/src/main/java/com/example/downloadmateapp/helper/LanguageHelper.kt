package com.example.downloadmateapp.helper

import android.content.Context
import android.widget.ArrayAdapter
import android.widget.Spinner
import com.example.downloadmateapp.R

object LanguageHelper {

    fun setupLanguageSpinner(
        context: Context,
        spinner: Spinner,
        savedLang: String,
        onLanguageChanged: (String) -> Unit
    ) {
        val languages = listOf("Türkçe", "English")
        val adapter = ArrayAdapter(context, android.R.layout.simple_spinner_item, languages)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinner.adapter = adapter

        val initialPos = if (savedLang == "en") 1 else 0
        spinner.setSelection(initialPos)

        spinner.onItemSelectedListener = object : android.widget.AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: android.widget.AdapterView<*>, view: android.view.View?, pos: Int, id: Long) {
                val selectedLang = if (pos == 1) "en" else "tr"
                if (selectedLang != savedLang) {
                    onLanguageChanged(selectedLang)
                }
            }

            override fun onNothingSelected(parent: android.widget.AdapterView<*>) {}
        }
    }
}