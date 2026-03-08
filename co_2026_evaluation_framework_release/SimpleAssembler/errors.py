class AssemblerError(Exception):
    def __init__(self,lineno,message):
        self.lineno=lineno
        self.message=message
        super().__init__(f"Line {lineno}: {message}")
