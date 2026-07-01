@checkout
Feature: Mini Shop checkout
  As a shopper
  I want to complete a purchase with my email
  So that I receive an order confirmation

  Background:
    Given I am on the checkout page

  @smoke
  Scenario: Successful checkout with valid email
    When I enter email "qa@example.com"
    And I click Pay Now
    Then I should see the order confirmation

  @validation
  Scenario: Validation error when email is missing
    When I click Pay Now
    Then I should see the error "Email is required"

  @smoke
  Scenario: Cart total is displayed
    Then the cart total should be "$49.99"
