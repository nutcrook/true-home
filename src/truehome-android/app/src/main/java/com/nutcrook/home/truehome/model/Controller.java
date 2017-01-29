package com.nutcrook.home.truehome.model;

/**
 * Created by nutcrook on 29/01/2017.
 */

public class Controller {
    private float watts;
    private boolean status;
    private float temperature;
    private boolean stateSet;
    private String name;
    private int controllerId;

    public Controller(int controllerId, String name, float watts, boolean status,
                      boolean stateSet, float temperature) {
        this.controllerId = controllerId;
        this.name = name;
        this.stateSet = stateSet;
        this.watts = watts;
        this.temperature = temperature;
        this.status = status;
    }

    public void switchState() {
        this.status = !this.stateSet;
        if (!this.stateSet) {
            this.stateSet = true;
        }
    }

    public boolean getStatus() {
        return this.status;
    }

    public void setStatus(boolean status) {
        this.status = status;
        if (!this.stateSet) {
            this.stateSet = true;
        }
    }

    public boolean isStateSet() {
        return this.stateSet;
    }

    public float getWatts() {
        return this.watts;
    }

    public void setWatts(float watts) {
        this.watts = watts;
    }

    public float getTemperature() {
        return this.temperature;
    }

    public void setTemperature(float temperature) {
        this.temperature = temperature;
    }

    public String getName() {
        return this.name;
    }
}
