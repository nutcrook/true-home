package com.nutcrook.home.truehome.model;

import com.nutcrook.home.truehome.model.Controller;
import java.util.ArrayList;

/**
 * Created by nutcrook on 29/01/2017.
 */

public class Room {
    private String roomName;
    private int roomId;
    private ArrayList<Controller> controllers;

    public Room(String roomName, int roomId) {
        this.roomId = roomId;
        this.roomName = roomName;
        this.controllers = new ArrayList<Controller>();
    }

    public Room(String roomName, int roomId, ArrayList<Controller> controllers) {
        this.roomId = roomId;
        this.roomName = roomName;
        this.controllers = controllers;
    }

    public void setControllers(ArrayList<Controller> controllers) {
        if (controllers != null) {
            this.controllers = controllers;
        }
    }

    public ArrayList<Controller> getControllers() {
        return this.controllers;
    }

    public void addConroller(Controller controller) {
        if (controller != null) {
            this.controllers.add(controller);
        }
    }
}
