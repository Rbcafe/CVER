package com.hhh.pojo;

import java.util.Arrays;

public class User {

    private String name;
    private String[] hobbies = new String[]{"dance","basketball"};

    public User(String name, Integer age, String[] hobbies) {
        this.name = name;
        this.hobbies = hobbies;
    }

    public User() {
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    //public void setHobbies(String[] hobbies) {
    //    this.hobbies = hobbies;
    //}

    public String[] getHobbies() {
        return hobbies;
    }

}
