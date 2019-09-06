package com.automationqapractice.utils;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverException;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class PageLoad {
public static boolean isOnCorrectPage (WebDriver driver) {
		
		try
        {
            new WebDriverWait(driver, 10).until(ExpectedConditions.urlContains("#account-creation"));
        }
        catch (WebDriverException ex)
        {
            return false;
        }
        return true;		
	}
}

