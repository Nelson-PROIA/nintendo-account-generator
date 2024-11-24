from random import uniform, choice
from time import sleep
from typing import Dict, Any

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def sleep_random(upper_bound: float, lower_bound: float) -> None:
    """TODO Comment"""
    sleep(uniform(upper_bound, lower_bound))


class FormSubmitter:
    """TODO Comment"""

    TYPE_LOWER_BOUND = 0.05
    TYPE_UPPER_BOUND = 0.5

    NEXT_LOWER_BOUND = 1
    NEXT_UPPER_BOUND = 2

    def __init__(self, form, humanize: bool = False) -> None:
        """TODO Comment"""
        self._form = form
        self._humanize = humanize

    def submit_form(self, driver, data: Dict[str, Any]) -> None:
        """TODO Comment"""
        sleep_random(FormSubmitter.NEXT_LOWER_BOUND, FormSubmitter.NEXT_UPPER_BOUND)

        for name, configuration in self._form.items():
            value = data.get(name)
            self._fill_input(driver, configuration, value)

            if self._humanize:
                sleep_random(FormSubmitter.NEXT_LOWER_BOUND, FormSubmitter.NEXT_UPPER_BOUND)

    def _fill_input(self, driver, configuration: Dict[str, Any], value: str) -> None:
        """TODO Comment"""
        input_id = configuration.get('id')
        input_type = configuration.get('type')
        move_to = configuration.get('move_to')

        element = driver.find_element(By.ID, input_id)

        if self._humanize and move_to:
            self._move_to_element(driver, element)

        if input_type == 'text':
            self._type(element, value, self._humanize)
        elif input_type == 'check':
            if element.is_selected() != value:
                self._click(element)
        elif input_type == 'wrapped-check':
            parent_tag = configuration['parent_tag']
            parent_identifier_type = configuration['parent_identifier_type']
            parent_identifier = configuration['parent_identifier']

            identifier_symbol = '#' if parent_identifier_type == 'id' else '.'
            css_selector = f'{parent_tag}{identifier_symbol}{parent_identifier} input#{input_id}'
            xpath = f'./ancestor::{parent_tag}[contains(@{parent_identifier_type}, "{parent_identifier}")]'

            checkbox = driver.find_element(By.CSS_SELECTOR, css_selector)
            parent = checkbox.find_element(By.XPATH, xpath)

            if checkbox.is_selected() != value:
                self._click(parent)
        elif input_type == 'select':
            self._select(element, value)
        elif input_type == 'submit':
            self._click(element)
        else:
            raise RuntimeError(f'Error: Unsupported field type: {input_type}!')

    @staticmethod
    def _move_to_element(driver, element) -> None:
        """TODO Comment"""
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

    @staticmethod
    def _click(element) -> None:
        """TODO Comment"""
        element.click()

    @classmethod
    def _type(cls, element, text: str, humanize: bool = False) -> None:
        """TODO Comment"""
        for character in text:
            element.send_keys(character)

            if humanize:
                sleep_random(FormSubmitter.TYPE_LOWER_BOUND, FormSubmitter.TYPE_UPPER_BOUND)

    @staticmethod
    def _select(element, option: str) -> None:
        """TODO Comment"""
        select = Select(element)

        if option is None:
            valid_options = [opt for opt in select.options if opt.get_attribute('value') not in ('', None)]

            if not valid_options:
                raise ValueError('Error: No valid options available to select!')

            option = choice(valid_options).get_attribute('value')

        select.select_by_value(option)
