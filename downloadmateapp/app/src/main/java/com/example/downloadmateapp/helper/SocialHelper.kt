package com.example.downloadmateapp.helper

import android.app.Activity
import android.content.Intent
import android.widget.ImageButton
import com.example.downloadmateapp.R
import com.example.downloadmateapp.WebViewActivity

object SocialHelper {

    fun setupSocialButtons(
        activity: Activity,
        buttons: Map<ImageButton, String>
    ) {
        buttons.forEach { (button, url) ->
            button.setOnClickListener {
                val intent = Intent(activity, WebViewActivity::class.java)
                intent.putExtra("url", url)
                activity.startActivity(intent)
            }
        }
    }

    fun setIconsForTheme(
        activity: Activity,
        instagram: ImageButton,
        youtube: ImageButton,
        twitter: ImageButton
    ) {
        val isDark = activity.resources.configuration.uiMode and
                android.content.res.Configuration.UI_MODE_NIGHT_MASK ==
                android.content.res.Configuration.UI_MODE_NIGHT_YES

        val instagramIcon = if (isDark) R.drawable.ic_d_instagram else R.drawable.ic_instagram
        val youtubeIcon = if (isDark) R.drawable.ic_d_youtube else R.drawable.ic_youtube
        val twitterIcon = if (isDark) R.drawable.ic_d_twitter else R.drawable.ic_twitter

        instagram.setImageResource(instagramIcon)
        youtube.setImageResource(youtubeIcon)
        twitter.setImageResource(twitterIcon)

        if (!isDark) {
            val white = activity.getColor(android.R.color.white)
            instagram.setColorFilter(white)
            youtube.setColorFilter(white)
            twitter.setColorFilter(white)
        } else {
            instagram.imageTintList = null
            youtube.imageTintList = null
            twitter.imageTintList = null
        }
    }
}