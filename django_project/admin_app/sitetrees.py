from sitetree.utils import tree, item

# Be sure you defined `sitetrees` in your module.
sitetrees = (
  # Define a tree with `tree` function.
  tree('books', items=[
      # Then define items and their children with `item` function.
      item('Books', 'books-listing', children=[
          item('Book named "{{ book.title }}"', 'books-details', in_menu=False, in_sitetree=False),
          item('Add a book', 'books-add'),
          item('Edit "{{ book.title }}"', 'books-edit', in_menu=False, in_sitetree=False)
      ])
  ]),
)