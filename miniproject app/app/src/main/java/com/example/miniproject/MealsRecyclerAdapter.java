package com.example.miniproject;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.RecyclerView;

import com.squareup.picasso.Picasso;

import java.util.List;

public class MealsRecyclerAdapter extends RecyclerView.Adapter<MealsRecyclerAdapter.DataHolder> {

    List<Meal> mealList;
    Context context;

    public MealsRecyclerAdapter(Context c, List<Meal> m) {
        mealList = m;
        context = c;

    }

    @NonNull
    @Override
    public DataHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        LayoutInflater layoutInflater = LayoutInflater.from(context);
        View view = layoutInflater.inflate(R.layout.meal_recycler_item,null);

        return new DataHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull DataHolder holder, int position) {
        Meal meal = new Meal();
        meal = mealList.get(position);

        byte[] decodedString = Base64.decode(meal.pic,Base64.DEFAULT);
        Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString,0,decodedString.length);


        String s = meal.mealItems.get(0);
        for(int i=1;i<meal.mealItems.size();i++) {
            s+=", " + meal.mealItems.get(i);
        }

        holder.mealItems.setText(s);
//        holder.date.setText(meal.consumption.toString());
        holder.mealPic.setImageBitmap(decodedByte);

        holder.cardView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                Toast.makeText(context, "Touched list", Toast.LENGTH_SHORT).show();
                return false;
            }
        });
    }

    @Override
    public int getItemCount() {
        return mealList.size();
    }

    class DataHolder extends RecyclerView.ViewHolder {
        ImageView mealPic;
        TextView mealItems, date;
        CardView cardView;
        public DataHolder(View itemView) {
            super(itemView);
            mealPic = itemView.findViewById(R.id.meal_recycler_img);
            mealItems = itemView.findViewById(R.id.meal_recycler_food_list);
            date = itemView.findViewById(R.id.meal_recycler_food_time);
            cardView = itemView.findViewById(R.id.recycler_card_view);
        }
    }


}
