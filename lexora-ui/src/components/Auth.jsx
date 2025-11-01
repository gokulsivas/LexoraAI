import React, { useState } from 'react';
import { signup, signin, logout } from './authService';

export const AuthComponent = () => {
    const [mode, setMode] = useState('signin'); // 'signin' or 'signup'
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (mode === 'signup') {
                await signup(
                    formData.username,
                    formData.email,
                    formData.password,
                    formData.confirmPassword
                );
                alert('Signup successful! Redirecting to dashboard...');
                // Redirect to main app
            } else {
                await signin(formData.email, formData.password);
                alert('Signin successful! Redirecting to dashboard...');
                // Redirect to main app
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px' }}>
            <h2>{mode === 'signin' ? 'Sign In' : 'Sign Up'}</h2>

            {error && <p style={{ color: 'red' }}>{error}</p>}

            <form onSubmit={handleSubmit}>
                {mode === 'signup' && (
                    <input
                        type="text"
                        name="username"
                        placeholder="Username"
                        value={formData.username}
                        onChange={handleChange}
                        required
                        style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
                    />
                )}

                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
                />

                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
                />

                {mode === 'signup' && (
                    <input
                        type="password"
                        name="confirmPassword"
                        placeholder="Confirm Password"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        required
                        style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
                    />
                )}

                <button
                    type="submit"
                    disabled={loading}
                    style={{
                        width: '100%',
                        padding: '10px',
                        backgroundColor: '#007bff',
                        color: 'white',
                        border: 'none',
                        cursor: 'pointer'
                    }}
                >
                    {loading ? 'Loading...' : mode === 'signin' ? 'Sign In' : 'Sign Up'}
                </button>
            </form>

            <button
                onClick={() => setMode(mode === 'signin' ? 'signup' : 'signin')}
                style={{ marginTop: '10px', width: '100%', padding: '10px' }}
            >
                {mode === 'signin' ? 'Create Account' : 'Already have an account?'}
            </button>
        </div>
    );
};
