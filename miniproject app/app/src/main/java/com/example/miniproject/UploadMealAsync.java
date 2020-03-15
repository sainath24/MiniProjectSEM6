package com.example.miniproject;

import android.os.AsyncTask;
import android.util.Log;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class UploadMealAsync extends AsyncTask<Meal,Void, String> {

    OkHttpClient httpClient;
    Response response;


    @Override
    protected String doInBackground(Meal... meals) {
        MediaType JSON = MediaType.get("application/json; charset=utf-8");

        String url = "http://192.168.43.15:4444/uploadmeal";

        OkHttpClient.Builder builder = new OkHttpClient.Builder();
        builder.connectTimeout(45, TimeUnit.SECONDS);
        builder.readTimeout(45, TimeUnit.SECONDS);
        builder.writeTimeout(45, TimeUnit.SECONDS);
        httpClient = builder.build();

        try {
            Gson gson = new Gson();
            String json = gson.toJson(meals[0]);

            RequestBody requestBody = RequestBody.create(json, JSON);
            Request request = new Request.Builder()
                    .url(url)
                    .post(requestBody)
                    .build();

            response = httpClient.newCall(request).execute();
            String s = response.body().string();


            JSONObject jsonObject = new JSONObject(s);
            JSONArray jsonArray = jsonObject.getJSONArray("food");
            meals[0].mealItems = new ArrayList<>();
            for(int i=0;i<jsonArray.length();i++) {
                meals[0].mealItems.add(jsonArray.getString(i));
            }
            MainActivity.mealList.add(meals[0]);
            return s;
        } catch (Exception e) {
            Log.i("UPLOAD_MEAL", e.toString());
            response = null;
        }
        return null;
    }

    @Override
    protected void onPostExecute(String s) {
        MainActivity.mealsRecyclerAdapter.notifyDataSetChanged();
//        Gson gson = new Gson();
//        String json = gson.toJson(response.body());
//        JSONObject jsonObject = new JSONObject();
//        //TODO:
//        //get json response and append to database and recycler

    }
}
