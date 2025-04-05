package com.example.downloadmateapp.helper

import android.content.Context
import android.widget.Toast

object ToastHelper {
    fun show(context: Context, resId: Int, vararg formatArgs: Any?) {
        Toast.makeText(context, context.getString(resId, *formatArgs), Toast.LENGTH_SHORT).show()
    }

    fun long(context: Context, resId: Int, vararg formatArgs: Any?) {
        Toast.makeText(context, context.getString(resId, *formatArgs), Toast.LENGTH_LONG).show()
    }

    fun show(context: Context, message: String) {
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show()
    }

    fun long(context: Context, message: String) {
        Toast.makeText(context, message, Toast.LENGTH_LONG).show()
    }


}