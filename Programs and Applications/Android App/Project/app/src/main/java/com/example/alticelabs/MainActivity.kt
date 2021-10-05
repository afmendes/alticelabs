package com.example.alticelabs

import android.os.Bundle
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val database = FirebaseDatabase.getInstance()


        val envHumidityView = findViewById<TextView>(R.id.environment_humidity_data)
        val envHumidity = database.getReference("windows_pc/data/environment/humidity")
        // Read from the database
        envHumidity.addValueEventListener(object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                val value = dataSnapshot.value
                envHumidityView.text = value.toString()
            }
            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
            }
        })

        val envBrightnessView = findViewById<TextView>(R.id.environment_brightness_data)
        val envBrightness = database.getReference("windows_pc/data/environment/brightness")
        // Read from the database
        envBrightness.addValueEventListener(object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                val value = dataSnapshot.value
                envBrightnessView.text = value.toString()
            }
            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
            }
        })

        val envTemperatureView = findViewById<TextView>(R.id.environment_temperature_data)
        val envTemperature = database.getReference("windows_pc/data/environment/temperature")
        // Read from the database
        envTemperature.addValueEventListener(object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                val value = dataSnapshot.value
                envTemperatureView.text = value.toString()
            }
            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
            }
        })

        val envNoiseView = findViewById<TextView>(R.id.environment_noise_data)
        val envNoise = database.getReference("windows_pc/data/environment/noise")
        // Read from the database
        envNoise.addValueEventListener(object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                val value = dataSnapshot.value
                envNoiseView.text = value.toString()
            }
            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
            }
        })

        val envCO2View = findViewById<TextView>(R.id.environment_co2_data)
        val envCO2 = database.getReference("windows_pc/data/environment/co2")
        // Read from the database
        envCO2.addValueEventListener(object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                val value = dataSnapshot.value
                envCO2View.text = value.toString()
            }
            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
            }
        })

        val userBPMView = findViewById<TextView>(R.id.user_bpm_data)
        val userBPM = database.getReference("windows_pc/data/user/bpm")
        // Read from the database
        userBPM.addValueEventListener(object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                val value = dataSnapshot.value
                userBPMView.text = value.toString()
            }
            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
            }
        })

        val userRespirationView = findViewById<TextView>(R.id.user_respiration_data)
        val userRespiration = database.getReference("windows_pc/data/user/respiration_rate")
        // Read from the database
        userRespiration.addValueEventListener(object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                val value = dataSnapshot.value
                userRespirationView.text = value.toString()
            }
            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
            }
        })

        val userTemperatureView = findViewById<TextView>(R.id.user_temperature_data)
        val userTemperature = database.getReference("windows_pc/data/user/body_temperature")
        // Read from the database
        userTemperature.addValueEventListener(object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                val value = dataSnapshot.value
                userTemperatureView.text = value.toString()
            }
            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
            }
        })

        val userPositionViewFront = findViewById<ImageView>(R.id.image_front_view)
        val userPositionViewSide = findViewById<ImageView>(R.id.image_side_view)
        val userPosition = database.getReference("windows_pc/data/user/position")
        // Read from the database
        userPosition.addValueEventListener(object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                val value = dataSnapshot.value.toString()
                when (value) {
                    "1" -> {
                        userPositionViewFront.setImageResource(R.drawable.sentado_direito)
                        userPositionViewSide.setImageResource(R.drawable.inclinado_direito)
                    }
                    "2" -> {
                        userPositionViewFront.setImageResource(R.drawable.sentado_direito)
                        userPositionViewSide.setImageResource(R.drawable.inclinado_frente)
                    }
                    "3" -> {
                        userPositionViewFront.setImageResource(R.drawable.sentado_direito)
                        userPositionViewSide.setImageResource(R.drawable.inclinado_frente)
                    }
                    "4" -> {
                        userPositionViewFront.setImageResource(R.drawable.sentado_direito)
                        userPositionViewSide.setImageResource(R.drawable.inclinado_tras)
                    }
                    "5" -> {
                        userPositionViewFront.setImageResource(R.drawable.inclinado_direita)
                        userPositionViewSide.setImageResource(R.drawable.inclinado_direito)
                    }
                    "6" -> {
                        userPositionViewFront.setImageResource(R.drawable.inclinado_esquerda)
                        userPositionViewSide.setImageResource(R.drawable.inclinado_direito)
                    }
                    "7" -> {
                        userPositionViewFront.setImageResource(R.drawable.perna_direita_cruzada)
                        userPositionViewSide.setImageResource(R.drawable.inclinado_direito)
                    }
                    "8" -> {
                        userPositionViewFront.setImageResource(R.drawable.perna_esquerda_cruzada)
                        userPositionViewSide.setImageResource(R.drawable.inclinado_direito)
                    }
                    "9" -> {
                        userPositionViewFront.setImageResource(R.drawable.empty_front)
                        userPositionViewSide.setImageResource(R.drawable.empty_side)
                    }
                }

            }
            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
            }
        })


    }
}