from flask import redirect, render_template, url_for, flash, request,session, current_app
from shop import db, app, photos
from .forms import AddproductsForm
from .models import Brand, Category, Addproducts
import secrets, os


@app.route('/')
def home():
    page = request.args.get('page',1, type=int)
    products = Addproducts.query.filter(Addproducts.stock > 0).paginate(page=page, per_page=4)
    brands = Brand.query.join(Addproducts,(Brand.id== Addproducts.brand_id)).all()
    categories = Category.query.join(Addproducts, (Category.id==Addproducts.category_id)).all()
    return render_template('products/index.html', products=products, brands=brands, categories=categories)

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproducts.query.get_or_404(id)
    brands = Brand.query.join(Addproducts,(Brand.id== Addproducts.brand_id)).all()
    categories = Category.query.join(Addproducts, (Category.id==Addproducts.category_id)).all()
    return render_template('products/single_page.html', product=product, brands=brands, categories=categories)

@app.route('/brand/<int:id>')
def get_brand(id):
    get_b = Brand.query.filter_by(id=id).first_or_404()
    page = request.args.get('page',1, type=int)
    brand = Addproducts.query.filter_by(brand = get_b).paginate(page=page, per_page=4)
    brands = Brand.query.join(Addproducts,(Brand.id== Addproducts.brand_id)).all()
    categories = Category.query.join(Addproducts, (Category.id==Addproducts.category_id)).all()
    return render_template('products/index.html', brand=brand, brands=brands, categories=categories, get_b=get_b)

@app.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproducts.query.filter_by(category=get_cat).paginate(page=page, per_page=4)
    brands = Brand.query.join(Addproducts,(Brand.id== Addproducts.brand_id)).all()
    categories = Category.query.join(Addproducts, (Category.id==Addproducts.category_id)).all()
    return render_template('products/index.html', get_cat_prod=get_cat_prod, categories=categories, brands=brands, get_cat=get_cat)

@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    
    return render_template('products/addbrand.html', brands='brands')

@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = brand
        flash(f'Your brand has been updated.', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title = "Update Brand Page", updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was delete from your database', 'success')
        return redirect(url_for('admin'))   
    flash(f'The brand {brand.name} cannot be deleted', 'warning')
    return redirect(url_for('admin'))  

@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if request.method == 'POST':
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The Category {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcat'))
    
    return render_template('products/addbrand.html')

@app.route('/updatecat/<int:id>', methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecat.name = category
        flash(f'Your category has been updated.', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title = "Update Category Page", updatecat=updatecat)

@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddproductsForm(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.desc.data
        brand = int(request.form.get('brand'))
        category = int(request.form.get('category'))
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        addpro = Addproducts(name=name, price=price, discount=discount, stock=stock, colors=colors ,desc=desc ,brand_id=brand, category_id=category, image_1=image_1, image_2=image_2,image_3=image_3)

        db.session.add(addpro)
        flash(f'The product {name} has been added to your database','success')
        db.session.commit()
        return redirect(url_for('admin'))
    
    return render_template('products/addproduct.html', title="Add Product Page", form=form, brands=brands , categories=categories)

@app.route('/updateproduct/<int:id>', methods=['GET' , 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproducts.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = AddproductsForm(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.desc = form.desc.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.brand_id = brand
        product.category_id = category
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f'Your product has been updated.', 'success')
        return redirect('../admin')

    form.name.data = product.name
    form.price.data = product.price
    form.desc.data = product.desc
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories, product=product)

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproducts.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {{product.name}} was deleted from your record','success')
        return redirect(url_for('admin'))
    flash(f'Cannot delete the product','danger')
    return redirect(url_for('admin'))