package com.hhh.controller;

import com.hhh.pojo.User;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;


@Controller
public class HelloController {

    @RequestMapping(value = {"/hello","/"})
    public String hello(User user, Model model){
        model.addAttribute("user", user);
        model.addAttribute("name", user.getName());
        return "success";
    }
}
