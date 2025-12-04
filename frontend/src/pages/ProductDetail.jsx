import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { Star } from 'lucide-react';

const ProductDetail = () => {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_URL}/products/${id}`);
                setProduct(response.data);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch product details');
                setLoading(false);
            }
        };

        fetchProduct();
    }, [id]);

    if (loading) return <div className="text-center mt-20">Loading...</div>;
    if (error) return <div className="text-center mt-20 text-red-500">{error}</div>;
    if (!product) return <div className="text-center mt-20">Product not found</div>;

    return (
        <div className="bg-white">
            <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
                <div className="lg:grid lg:grid-cols-2 lg:gap-x-12">
                    {/* Image Gallery */}
                    <div className="product-image-gallery">
                        <div className="aspect-[3/4] w-full overflow-hidden bg-gray-100 rounded-lg">
                            <img
                                src={product.image_url}
                                alt={product.title}
                                className="h-full w-full object-cover object-center"
                            />
                        </div>
                    </div>

                    {/* Product Info */}
                    <div className="mt-10 lg:mt-0 lg:pl-8">
                        <nav aria-label="Breadcrumb" className="mb-4">
                            <ol role="list" className="flex items-center space-x-2">
                                <li>
                                    <Link to="/" className="text-sm font-medium text-gray-500 hover:text-gray-900">Home</Link>
                                </li>
                                <li>
                                    <svg width="16" height="20" viewBox="0 0 16 20" fill="currentColor" aria-hidden="true" className="h-5 w-4 text-gray-300">
                                        <path d="M5.697 4.34L8.98 16.532h1.327L7.025 4.341H5.697z" />
                                    </svg>
                                </li>
                                <li className="text-sm">
                                    <span aria-current="page" className="font-medium text-gray-900">{product.title}</span>
                                </li>
                            </ol>
                        </nav>

                        <h1 className="text-3xl font-bold tracking-tight text-gray-900 uppercase sm:text-4xl">{product.title}</h1>
                        <div className="mt-4">
                            <p className="text-2xl tracking-tight text-gray-900">₹{product.price}</p>
                        </div>

                        {/* Reviews */}
                        <div className="mt-4">
                            <div className="flex items-center">
                                <div className="flex items-center">
                                    {[0, 1, 2, 3, 4].map((rating) => (
                                        <Star
                                            key={rating}
                                            className={`h-5 w-5 flex-shrink-0 ${(product.features?.rating || 0) > rating ? 'text-gray-900' : 'text-gray-200'
                                                }`}
                                            fill="currentColor"
                                        />
                                    ))}
                                </div>
                                <span className="ml-3 text-sm font-medium text-gray-500">{product.features?.rating} stars</span>
                            </div>
                        </div>

                        <div className="mt-8">
                            <h3 className="sr-only">Description</h3>
                            <div className="space-y-6 text-base text-gray-700">
                                <p>{product.description || product.descriptions}</p>
                            </div>
                        </div>

                        {/* Highlights */}
                        <div className="mt-8 border-t border-gray-200 pt-8">
                            <h3 className="text-sm font-medium text-gray-900">Highlights</h3>
                            <div className="mt-4">
                                <ul role="list" className="list-disc space-y-2 pl-4 text-sm">
                                    {product.features?.attributes?.map((highlight) => (
                                        <li key={highlight} className="text-gray-600">
                                            <span className="text-gray-600">{highlight}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProductDetail;
