-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-12-2024 a las 21:23:49
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `servitec1`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id_item` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id_item`, `nombre`, `cantidad`, `descripcion`) VALUES
(1, 'Pantalla LCD', 24, 'Componente encargado de mostrar imagen lcd  y de interaccion tactil.'),
(2, 'Baterias', 43, 'Fuente de energia recargable segun su voltaje.'),
(3, 'Conector de carga', 45, 'Puerto fisico que permite cargar el dispositivo o transferir datos.'),
(4, 'Camaras(trasera,frontal)', 124, 'Modulos que capturan imagenes y videos.'),
(5, 'Microfono', 24, 'Componente que capta el sonido para llamadas y demas.'),
(6, 'Altavoz', 12, 'Componente que emite el sonido del dispositivo.'),
(7, 'Flex(cable)', 44, 'Cable flexible que conecta componentes internos.'),
(8, 'Carcasa', 100, 'Estructura externa que protege los componentes internos del dispositivo.'),
(9, 'Placas electronicas', 24, 'Circuitos integrados que controlan funciones especificas.'),
(10, 'Antena wi-fi/bluetooth', 55, 'Componenete que permite la conexion inalambrica del dispositivo.'),
(11, 'Lentes de camara', 12, 'Cubiertas protectoras de vidrio sobre los modulos de camara.'),
(12, 'Placa de carga', 36, 'Circuito integrado donde se encuentra el puerto de carga.'),
(13, 'Conector de SIM y microSD', 8, 'Bandejas internas donde se alojan la tarjeta SIM y microSD.'),
(14, 'Zocalo de memoria RAM', 28, 'Ranuras deonde se conectan los modulos de memoria.'),
(15, 'Conector de audifonos', 12, 'Puerto para conectar auriculares o equipos de sonido.'),
(16, 'Sensor de huella dactilar', 24, 'Componente utilizado para la autenticacion biometrica en dispositivos moviles.'),
(17, 'Pantallas Oled/Amoled', 50, 'Pantallas avanzadas en dispositivos moviles con placa base de laptop.'),
(18, 'Disipador de calor', 21, 'Disipa el calor generado por componentes como procesadores.'),
(19, 'Botones de power y volumen', 26, 'Controladores fisicos para moviles.'),
(20, 'Sensor de proximidad', 24, 'Detecta la proximidad del usuario o realiza funciones de control de gestos.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordenes`
--

CREATE TABLE `ordenes` (
  `id_orden` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_tecnico` int(11) DEFAULT NULL,
  `descripcion` text NOT NULL,
  `marca` varchar(50) NOT NULL,
  `estado` enum('Pendiente','En Proceso','Completada') DEFAULT 'Pendiente',
  `monto` decimal(10,2) DEFAULT 0.00,
  `f_ingreso` date DEFAULT NULL,
  `f_entrega` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ordenes`
--

INSERT INTO `ordenes` (`id_orden`, `id_cliente`, `id_tecnico`, `descripcion`, `marca`, `estado`, `monto`, `f_ingreso`, `f_entrega`, `created_at`, `updated_at`) VALUES
(1, 6, 5, 'pantalla rota', 'samsung a20s', 'Completada', 180.00, '2024-12-09', '2024-12-11', '2024-12-09 16:56:05', '2024-12-10 18:23:28'),
(2, 6, NULL, 'Mi celular ya no recibe carga rapida con su cargador original.', 'xiaomi redmi note 13pro', 'Pendiente', 0.00, NULL, NULL, '2024-12-10 18:32:34', '2024-12-10 18:32:34'),
(3, 9, 8, 'Tengo mi celular todo sulfateado ya que lo hice caer al agua', 'ssamsung a10s', 'En Proceso', 200.00, '2024-12-11', NULL, '2024-12-10 19:45:44', '2024-12-10 19:52:58');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `id_pago` int(11) NOT NULL,
  `id_orden` int(11) NOT NULL,
  `monto_pagado` decimal(10,2) NOT NULL,
  `fecha_pago` timestamp NOT NULL DEFAULT current_timestamp(),
  `metodo_pago` varchar(50) DEFAULT 'Efectivo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`id_pago`, `id_orden`, `monto_pagado`, `fecha_pago`, `metodo_pago`) VALUES
(1, 1, 180.00, '2024-12-19 04:00:00', 'Tarjeta de Crédito');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `nombre`, `descripcion`) VALUES
(1, 'Administrador', 'Acceso completo al sistema'),
(2, 'Técnico', 'Acceso a gestión de órdenes y productos'),
(3, 'Cliente', 'Acceso a la creación de órdenes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `id_rol` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `email`, `contrasena`, `telefono`, `id_rol`) VALUES
(4, 'limbert', 'limbert123@gmail.com', '1234', '77745198', 1),
(5, 'evelyn', 'evelyn69@gmail.com', '12345', '67674545', 2),
(6, 'weymar', 'weymar24@gmail.com', '123456', '78456734', 3),
(8, 'carlitos', 'carlitos123@gmail.com', '123', '78782323', 2),
(9, 'lea', 'lea12@gmail.com', '12', '78782433', 3);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id_item`);

--
-- Indices de la tabla `ordenes`
--
ALTER TABLE `ordenes`
  ADD PRIMARY KEY (`id_orden`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_tecnico` (`id_tecnico`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `id_orden` (`id_orden`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id_item` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `ordenes`
--
ALTER TABLE `ordenes`
  MODIFY `id_orden` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ordenes`
--
ALTER TABLE `ordenes`
  ADD CONSTRAINT `ordenes_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `ordenes_ibfk_2` FOREIGN KEY (`id_tecnico`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL;

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_orden`) REFERENCES `ordenes` (`id_orden`) ON DELETE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
