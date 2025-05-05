package com.example.downloadmateapp.helper

object PlatformDetector {
    fun detectPlatformFromUrl(url: String): String {
        val lowercaseUrl = url.lowercase()
        return when {
            "youtube.com" in lowercaseUrl || "youtu.be" in lowercaseUrl -> "youtube"
            "instagram.com" in lowercaseUrl -> "instagram"
            "twitter.com" in lowercaseUrl || "x.com" in lowercaseUrl -> "twitter"
            "tiktok.com" in lowercaseUrl -> "tiktok"
            "facebook.com" in lowercaseUrl -> "facebook"
            else -> ""
        }
    }
}