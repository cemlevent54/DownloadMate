package com.example.downloadmateapp.helper

import android.content.Context
import android.content.res.Configuration
import androidx.appcompat.app.AppCompatDelegate

object ThemeHelper {

    private const val KEY_THEME_MODE = "theme_mode"

    fun applySavedTheme(context: Context) {
        val mode = PrefsHelper.getInt(context, KEY_THEME_MODE, AppCompatDelegate.MODE_NIGHT_NO)
        AppCompatDelegate.setDefaultNightMode(mode)
    }

    fun saveTheme(context: Context, mode: Int) {
        PrefsHelper.saveInt(context, KEY_THEME_MODE, mode)
    }

    fun isNightMode(context: Context): Boolean {
        val currentNightMode = context.resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK
        return currentNightMode == Configuration.UI_MODE_NIGHT_YES
    }

}