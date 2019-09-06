package com.automationqapractice.utils;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.ie.InternetExplorerDriver;
import io.github.bonigarcia.wdm.WebDriverManager;



public class Webdriverfactory {

	    public static WebDriver createWebDriver(String browser) {

	        if (browser.toString().equalsIgnoreCase("firefox")) {

	            return new FirefoxDriver();
	        } else if (browser.toString().equalsIgnoreCase("ie")) {

	            return new InternetExplorerDriver();
	        } else if (browser.toString().equalsIgnoreCase("chrome")) {
	        	WebDriverManager.chromedriver().version("76.0.3809.126").setup();
	            return new ChromeDriver();
	        }
	        throw new IllegalArgumentException(
	            "Supplied WebDriver type is not understood. Please refer to " + Webdriverfactory.class.getName());
	    }

}

