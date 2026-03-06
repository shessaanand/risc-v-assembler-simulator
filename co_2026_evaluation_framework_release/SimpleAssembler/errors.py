class AssemblerError(Exception):
    def __init__(self,lineNumber,message):
        self.lineNumber=lineNumber
        self.message=message
        super().__init__(f"Line {lineNumber}: {message}")
