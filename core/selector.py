import re

class Selector:
    def __init__(self, xml_root):
        self.root = xml_root

    def find(self, target_config):
        """
        Ищет элемент по списку стратегий.
        Пример target_config:
        {
            "strategies": [
                {"type": "id", "value": "com.instagram:id/login"},
                {"type": "text", "value": "Войти"},
                {"type": "desc", "value": "Login button"}
            ]
        }
        """
        strategies = target_config.get("strategies", [])
        
        for strategy in strategies:
            st_type = strategy.get("type")
            st_value = strategy.get("value")
            
            # Пробегаем по всем узлам XML дерева
            for node in self.root.iter():
                found = False
                
                if st_type == "id":
                    # resource-id может быть длинным, проверяем вхождение
                    if st_value in node.get("resource-id", ""):
                        found = True
                        
                elif st_type == "text":
                    # Игнорируем регистр
                    if st_value.lower() in node.get("text", "").lower():
                        found = True
                        
                elif st_type == "desc":
                    if st_value.lower() in node.get("content-desc", "").lower():
                        found = True

                if found:
                    return self._get_center(node.get("bounds"))
        
        return None

    def _get_center(self, bounds_str):
        """Превращает '[0,0][100,200]' в (50, 100)"""
        try:
            coords = list(map(int, re.findall(r'\d+', bounds_str)))
            if len(coords) == 4:
                x = (coords[0] + coords[2]) // 2
                y = (coords[1] + coords[3]) // 2
                return x, y
        except:
            pass
        return None