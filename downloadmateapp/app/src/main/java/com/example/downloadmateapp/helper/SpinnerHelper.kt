package com.example.downloadmateapp.helper

import android.content.Context
import android.graphics.Color
import android.widget.ArrayAdapter
import android.widget.Spinner
import com.example.downloadmateapp.R

object SpinnerHelper {

    fun setupPlatformAndTypeSpinners(
        context: Context,
        spinnerPlatform: Spinner,
        spinnerType: Spinner,
        isNightMode: Boolean,
        setDownloadButtonColor: (Int, Int?) -> Unit
    ) {
        val platforms = listOf(
            context.getString(R.string.select_option),
            context.getString(R.string.platform_youtube),
            context.getString(R.string.platform_instagram),
            context.getString(R.string.platform_twitter)
        )

        val types = listOf(
            context.getString(R.string.select_option),
            context.getString(R.string.type_video),
            context.getString(R.string.type_audio)
        )

        spinnerPlatform.adapter = ArrayAdapter(context, android.R.layout.simple_spinner_item, platforms)
            .also { it.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item) }

        spinnerType.adapter = ArrayAdapter(context, android.R.layout.simple_spinner_item, types)
            .also { it.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item) }

        spinnerPlatform.setOnItemSelectedListener(object : android.widget.AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: android.widget.AdapterView<*>, view: android.view.View?, pos: Int, id: Long) {
                val selected = parent.getItemAtPosition(pos).toString().lowercase()

                when (selected) {
                    context.getString(R.string.platform_youtube).lowercase() -> setDownloadButtonColor(Color.parseColor("#FF0000"), null)
                    context.getString(R.string.platform_twitter).lowercase() -> setDownloadButtonColor(Color.parseColor("#1DA1F2"), null)
                    context.getString(R.string.platform_instagram).lowercase() -> setDownloadButtonColor(Color.parseColor("#c13584"), null)
                    context.getString(R.string.select_option).lowercase() -> {
                        val bgColor = if (isNightMode) Color.WHITE else Color.BLACK
                        val textColor = if (isNightMode) Color.BLACK else Color.WHITE
                        setDownloadButtonColor(bgColor, textColor)
                    }
                }
            }

            override fun onNothingSelected(parent: android.widget.AdapterView<*>) {}
        })
    }
}