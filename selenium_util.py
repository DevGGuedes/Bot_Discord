from __future__ import annotations
import itertools
import re
import sys
import time
import traceback
import unicodedata
from enum import IntEnum
from io import BytesIO
from typing import Optional, Callable, Generic, TypeVar, List
from subprocess import Popen, PIPE
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException
import selenium
import selenium.webdriver as wd
from PIL import Image
from io import BytesIO
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

T = TypeVar('T')
U = TypeVar('U')
TU = TypeVar('TU')

class QueryFn(Generic[T]):
    fn: Callable[[], Optional[T]]

    def __init__(self, fn: Callable[[], Optional[T]]):
        self.fn = fn

    def __call__(self) -> Optional[T]:
        return self.fn()

    def filter(self, predicate: Callable[[T], bool]) -> QueryFn[T]:
        def newfn() -> Optional[T]:
            result = self()
            if result is not None and predicate(result):
                return result
            return None
        return QueryFn(newfn)
    
    def map(self, mapper: Callable[[T], U]) -> QueryFn[U]:
        def newfn() -> Optional[U]:
            result = self()
            if result is None:
                return None
            return map(result)
        return QueryFn(newfn)
    
    def and_not(self, other: QueryFn[U]) -> QueryFn[T]:
        def newfn() -> Optional[T]:
            result = other()
            if result is None:
                return self()
            return None
        return QueryFn(newfn)
    
    def and_(self, other: QueryFn[U]) -> QueryFn[U]:
        def newfn() -> Optional[U]:
            result = self()
            if result is None:
                return None
            return other()
        return QueryFn(newfn)
    
    def not_(self) -> QueryFn[None]:
        def newfn() -> Optional[U]:
            result = self()
            if result is not None:
                return None
            return [None]
        return QueryFn(newfn)
    
    def and_then(self, other: Callable[[T], QueryFn[U]]) -> QueryFn[U]:
        def newfn() -> Optional[U]:
            result = self()
            if result is None:
                return None
            return other(result)()
        return QueryFn(newfn)
    
    def or_(self, other: QueryFn[U]) -> Query[Union[T,U]]:
        def newfn() -> Optional[Union[T,U]]:
            result = self()
            if result is None:
                return other()
            return self()
        return QueryFn(newfn)
    
    def zip_with(self, other: QueryFn[U], zipper: Callable[[T, U], TU]) -> QueryFn[TU]:
        def newfn() -> Optional[TU]:
            t = self()
            if t is None:
                return None
            u = other()
            if u is None:
                return None
            return zipper(t, u)
        return QueryFn(newfn)

class Query:
    driver: Union[WebDriver, WebElement]

    def __init__(self, root):
        self.driver = root

    @staticmethod
    def _get_one(fn: Callable[[], T]) -> Callable[[], Optional[T]]:
        def newfn():
            try:
                return fn()
            except NoSuchElementException as e:
                if type(e) != NoSuchElementException:
                    raise
                return None
        return newfn
    
    @staticmethod
    def _get_all(fn: Callable[[], List[T]]) -> Callable[[], List[Optional[T]]]:
        def newfn():
            result =  fn()
            if len(result) == 0:
                return None
            return result
        return newfn

    def by_id(self, eid) -> QueryFn[WebElement]:
        return QueryFn(Query._get_one(lambda: self.driver.find_element_by_id(eid)))

    def by_id_all(self, eid) -> QueryFn[List[WebElement]]:
        return QueryFn(Query._get_all(lambda: self.driver.find_elements_by_id(eid)))
    
    def by_css_selector(self, selector) -> QueryFn[WebElement]:
        return QueryFn(Query._get_one(lambda: self.driver.find_element_by_css_selector(selector)))

    def by_css_selector_all(self, selector) -> QueryFn[List[WebElement]]:
        return QueryFn(Query._get_all(lambda: self.driver.find_elements_by_css_selector(selector)))

    def by_xpath(self, selector) -> QueryFn[WebElement]:
        return QueryFn(Query._get_one(lambda: self.driver.find_element_by_xpath(selector)))

    def by_xpath_all(self, selector) -> QueryFn[List[WebElement]]:
        return QueryFn(Query._get_all(lambda: self.driver.find_elements_by_xpath(selector)))

def aguardar_query(query_fn: QueryFn[Union[WebElement, List[WebElement]]], interval=0.001, timeout=10_000) -> List[WebElement] | WebElement:
    if timeout != None:
        started = time.perf_counter_ns()
        timeout = int(timeout * 1_000_000)
    while True:
        if timeout != None:
            if time.perf_counter_ns() - started > timeout:
                raise TimeoutError()

        try:
            elementos = query_fn()

            if elementos is not None:
                return elementos
        except StopIteration:
            pass
        except Exception as e:
            if type(e) == NoSuchWindowException:
                raise
            traceback.print_exc()

        time.sleep(interval)

def aguardar_queryfn(query_fn: QueryFn[Union[T, List[T]]], interval=0.001, timeout=10_000) -> List[T] | T:
    if timeout != None:
        started = time.perf_counter_ns()
        timeout = int(timeout * 1_000_000)
    while True:
        if timeout != None:
            if time.perf_counter_ns() - started > timeout:
                raise TimeoutError()

        try:
            elementos = query_fn()

            if elementos is not None:
                return elementos
        except StopIteration:
            pass

        time.sleep(interval)

