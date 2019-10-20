from zope.interface import provider
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model, directives
from plone.namedfile.field import NamedBlobImage
from zope import schema


@provider(IFormFieldProvider)
class IMegaMenuImages(model.Schema):
    directives.fieldset(
        'megamenuimages',
        label=u'Mega Menu Images',
        fields=(
            'navigation_image',
            'teaser_image',
            'teaser_background'
        )
    )

    navigation_image = NamedBlobImage(
        title=u'Navigation Image'
    )

    teaser_image = NamedBlobImage(
        title=u'Teaser Image'
    )

    teaser_background = NamedBlobImage(
        title=u'Teaser Background'
    )


@provider(IFormFieldProvider)
class IMegaMenuContainer(model.Schema):
    directives.fieldset(
        'megamenucontainer',
        label=u'Mega Menu Container',
        fields=('is_mega_menu',)
    )

    is_mega_menu = schema.Bool(
        title=u'Is Mega Menu'
    )
