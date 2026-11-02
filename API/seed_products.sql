DELETE FROM products;
ALTER SEQUENCE products_id_seq RESTART WITH 1;

INSERT INTO products (name, description, details, price, category, image_url, stock) VALUES
('Espresso', 'Rich and intense single shot.', 'Made from 100% arabica beans, medium-dark roast.', 3.50, 'Coffee', 'https://placehold.co/600x800/EAE5DF/1A1A1A/png?text=Espresso', 100),
('Cappuccino', 'Espresso with steamed milk and foam.', 'Classic Italian cappuccino with a velvety milk foam.', 4.75, 'Coffee', 'https://placehold.co/600x800/EAE5DF/1A1A1A/png?text=Cappuccino', 100),
('Latte', 'Smooth espresso with plenty of steamed milk.', 'Served hot, mild and creamy.', 5.00, 'Coffee', 'https://placehold.co/600x800/EAE5DF/1A1A1A/png?text=Latte', 100),
('Flat White', 'Double espresso with silky microfoam.', 'Stronger than a latte, smoother than a cappuccino.', 5.25, 'Coffee', 'https://placehold.co/600x800/EAE5DF/1A1A1A/png?text=Flat%20White', 80),
('Cold Brew', 'Slow-steeped coffee served over ice.', 'Brewed for 18 hours, low acidity.', 5.50, 'Coffee', 'https://placehold.co/600x800/EAE5DF/1A1A1A/png?text=Cold%20Brew', 60),
('Green Tea', 'Light and refreshing loose-leaf tea.', 'Sencha green tea, served with honey on request.', 3.75, 'Tea', 'https://placehold.co/600x800/EAE5DF/1A1A1A/png?text=Green%20Tea', 70),
('Croissant', 'Buttery, flaky and freshly baked.', 'Baked every morning.', 3.25, 'Pastries', 'https://placehold.co/600x800/EAE5DF/1A1A1A/png?text=Croissant', 40),
('Cheesecake Slice', 'Creamy cheesecake with berry sauce.', 'Homemade, served chilled.', 6.50, 'Pastries', 'https://placehold.co/600x800/EAE5DF/1A1A1A/png?text=Cheesecake', 25);
