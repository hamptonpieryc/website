from html_transformer import Transform, Transformer, NestedTransform, TransformingParser, DomTransformer, \
    CaptureElementsParser


class FooTransform(Transform):
    def __init__(self):
        Transform.__init__(self=self, outer_tag="foo")

    def transform(self, nodes: list) -> str:
        result = ''
        for node in nodes:
            if node['tag'] == 'p':
                result += '<div>' + node['inner_html'].upper() + '</div>'
        return result


class BarTransform(Transform):

    def __init__(self):
        self.outer_tag = "bar"

    def transform(self, nodes: list) -> str:
        result = ''
        for node in nodes:
            if node['tag'] == 'header':
                result += '<h1>' + node['inner_html'].upper() + '</h1>'
        return result


def test_should_transform_foo_content():
    raw = '<foo><p>Foo</p></foo>'
    expected = '<div>FOO</div>'

    transformer = Transformer(FooTransform())
    assert transformer.transform(raw) == expected


def test_should_preserve_if_no_transform():
    raw = '<not-foo><p>Foo</p></not-foo>'
    expected = '<not-foo><p>Foo</p></not-foo>'

    transformer = Transformer(FooTransform())
    assert transformer.transform(raw) == expected


def test_should_transform_nested_content():
    raw = '<nested><foo><p>Foo</p></foo></nested>'
    expected = '<div>FOO</div>\n'

    nested = NestedTransform(outer_tag='nested', transforms=[FooTransform()])
    transformer = Transformer(nested)
    transformer.transform(raw)
    assert transformer.transform(raw) == expected


def test_should_apply_single_transformer_to_html():
    raw_html = """
         <html>
         <body>
             <foo><p>Foo</p></foo>
         </body>
         </html>"""

    output_html = """
         <html>
         <body>
             <div>FOO</div>
         </body>
         </html>"""

    buffer = []
    parser = TransformingParser(buffer, [FooTransform()])
    parser.feed(raw_html)
    assert ''.join(buffer) == output_html


def test_should_apply_multiple_transformers_to_html():
    raw_html = """
         <html>
         <body>
             <foo><p>Foo</p></foo>
             <bar><header>Hello World</header></bar>
             <leave-me-alone-content>I want to be alone</leave-me-alone-content>
         </body>
         </html>"""

    output_html = """
         <html>
         <body>
             <div>FOO</div>
             <h1>HELLO WORLD</h1>
             <leave-me-alone-content>I want to be alone</leave-me-alone-content>
         </body>
         </html>"""

    buffer = []
    parser = TransformingParser(buffer, [FooTransform(), BarTransform()])
    parser.feed(raw_html)
    assert ''.join(buffer) == output_html


def test_should_produce_lookup_of_captured_elements():
    raw_html = """
               <html>
               <body>
                   <foo><p>Foo</p></foo>
                   <bar class="wibble">BAR</bar>
               </body>
               </html>"""

    expected = [('foo', '<p>Foo</p>', {}), ('bar', 'BAR', {'class': 'wibble'})]

    parser = CaptureElementsParser(['foo', 'bar'])
    parser.feed(raw_html)
    assert expected == parser.captured



def test_should_apply_nested_transformers():
    raw_html = """
            <html>
            <body>
                <nested>
                    <foo><p>Foo</p></foo>
                    <foo><p>Boo</p></foo>
                    <p>skip me</p>
                    <bar><header>Hello World</header></bar>
                </nested>
            </body>
            </html>"""

    # note - the current implementation does not preserve leading whitespace nicely
    output_html = """
            <html>
            <body>
                <div>FOO</div>
<div>BOO</div>
<h1>HELLO WORLD</h1>

            </body>
            </html>"""

    nested = NestedTransform(outer_tag='nested', transforms=[FooTransform(), BarTransform()])
    buffer = []
    parser = TransformingParser(buffer, [nested])
    parser.feed(raw_html)
    assert ''.join(buffer) == output_html


def test_should_convert_html_to_domlike():
    raw_html = """
                <container>
                    <span>a span</span>
                    <span class="foo">a span with class</span>
                    <div>a div with <span class="nested">nested</span> span</div>
                </container>"""

    transformer = DomTransformer("container")
    dom = transformer.transform(raw_html)
    assert len(dom) == 3
    span1 = dom[0]
    assert span1["tag"] == "span"
    assert span1["inner_html"] == "a span"
    span2 = dom[1]
    assert span2["tag"] == "span"
    assert span2["inner_html"] == "a span with class"
    div1 = dom[2]
    assert div1["tag"] == "div"
    assert div1["inner_html"] == "a div with <span class=\"nested\">nested</span> span"
