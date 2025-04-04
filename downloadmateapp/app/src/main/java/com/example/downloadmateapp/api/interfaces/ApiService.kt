package com.example.downloadmateapp.network

import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST

data class DownloadRequest(
    val url: String,
    val type: String
)

interface ApiService {
    @POST("/youtube/download")
    suspend fun downloadYoutube(
        @Body request: DownloadRequest,
        @Header("Cookie") cookies: String? = null
    ): Response<ResponseBody>

    @POST("/instagram/download")
    suspend fun downloadInstagram(
        @Body request: DownloadRequest,
        @Header("Cookie") cookie: String?
    ): Response<ResponseBody>

    @POST("/twitter/download")
    suspend fun downloadTwitter(
        @Body request: DownloadRequest,
        @Header("Cookie") cookie: String?
    ): Response<ResponseBody>
}