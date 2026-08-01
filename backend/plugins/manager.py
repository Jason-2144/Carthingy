import importlib
import pkgutil
import os
from typing import Dict, Any, Type
from backend.scraper.core.base import BaseScraper

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, Type[BaseScraper]] = {}
        
    def discover_plugins(self, package_name: str = "backend.plugins"):
        """
        Dynamically loads marketplace scrapers placed in the plugins folder.
        """
        # This is a conceptual implementation. 
        # In reality we iterate over modules in backend.plugins
        # and look for classes inheriting from BaseScraper.
        try:
            plugin_module = importlib.import_module(package_name)
            for _, name, _ in pkgutil.iter_modules(plugin_module.__path__):
                mod = importlib.import_module(f"{package_name}.{name}")
                for attr_name in dir(mod):
                    attr = getattr(mod, attr_name)
                    if isinstance(attr, type) and issubclass(attr, BaseScraper) and attr is not BaseScraper:
                        self.register_plugin(attr.marketplace, attr)
        except Exception as e:
            print(f"Plugin discovery failed: {e}")
            
    def register_plugin(self, marketplace_name: str, scraper_class: Type[BaseScraper]):
        self.plugins[marketplace_name.upper()] = scraper_class
        
    def get_scraper(self, marketplace_name: str) -> Type[BaseScraper]:
        return self.plugins.get(marketplace_name.upper())
        
    def get_registered_marketplaces(self) -> list:
        return list(self.plugins.keys())

plugin_manager = PluginManager()
