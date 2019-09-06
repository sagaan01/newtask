package com.automationqapractice.base;

public enum Dresscategory {
	PRINTED_SUMMER_DRESS ("Printed Summer Dress"),
	PRINTED_DRESS("Printed Dress"),
	PRINTED_SCHIFFON_DRESS("Printed Chiffon Dress"),
	INVALID_CATEGORY("Invalid");
	
	
	private String name;

	Dresscategory(String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    } 

}