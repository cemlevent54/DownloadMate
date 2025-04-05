package com.example.downloadmateapp.helper

import android.content.Context
import android.content.res.Configuration
import java.util.*

object LocaleHelper {

    private const val PREFS_NAME = "app_preferences"
    private const val LANGUAGE_KEY = "selected_language"

    fun applySavedLocale(context: Context): Context {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val lang = prefs.getString(LANGUAGE_KEY, "tr") ?: "tr"
        val locale = Locale(lang)
        Locale.setDefault(locale)

        val config = Configuration(context.resources.configuration)
        config.setLocale(locale)

        return context.createConfigurationContext(config)
    }

    fun saveLocale(context: Context, languageCode: String) {
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            .edit().putString(LANGUAGE_KEY, languageCode).apply()
    }
}
