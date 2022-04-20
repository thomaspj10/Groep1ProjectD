class Page:
    
    name: str
    authentication_level: int
    create_page: callable
    
    def __init__(self, name: str, authentication_level: int, create_page: callable) -> None:
        self.name = name
        self.authentication_level = authentication_level
        self.create_page = create_page