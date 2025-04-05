package com.example.downloadmateapp.api

import com.example.downloadmateapp.network.ApiService
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object RetrofitClient {
    private const val BASE_URL = "https://local-pippa-downloadmate-82e1c8e1.koyeb.app/"

    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val client = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(60, TimeUnit.SECONDS)  // ⏱ Bağlantı için bekleme süresi
        .readTimeout(120, TimeUnit.SECONDS)    // ⏱ Veri okuma süresi
        .writeTimeout(120, TimeUnit.SECONDS)   // ⏱ Veri yazma süresi (request body vs.)
        .build()

    val apiService: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}
