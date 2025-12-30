# -*- coding: utf-8 -*-

import sys
import mysql.connector as mc
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QLineEdit, QPushButton,
                              QTableWidget, QTableWidgetItem, QGroupBox, QStatusBar,
                              QMessageBox)
from PyQt6.QtCore import Qt
import pandas as pd

from keyword_selector import CheckableComboBox


class ScanResultsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scan Results Viewer")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # === Database Configuration Group ===
        db_group = QGroupBox("Database Configuration")
        db_group_layout = QVBoxLayout()
        
        # Database name input
        db_layout = QHBoxLayout()
        db_label = QLabel("Database:")
        db_label.setMinimumWidth(120)
        self.lineEditDb = QLineEdit()
        self.lineEditDb.setPlaceholderText("Enter database name")
        db_layout.addWidget(db_label)
        db_layout.addWidget(self.lineEditDb)
        db_group_layout.addLayout(db_layout)
        
        # Table name input
        table_layout = QHBoxLayout()
        table_label = QLabel("Table:")
        table_label.setMinimumWidth(120)
        self.lineEditTable = QLineEdit()
        self.lineEditTable.setPlaceholderText("Enter table name")
        table_layout.addWidget(table_label)
        table_layout.addWidget(self.lineEditTable)
        db_group_layout.addLayout(table_layout)
        
        db_group.setLayout(db_group_layout)
        main_layout.addWidget(db_group)
        
        # === Search Criteria Group ===
        search_group = QGroupBox("Search Criteria")
        search_group_layout = QVBoxLayout()
        
        # Path search input
        path_layout = QHBoxLayout()
        path_label = QLabel("Mount Path:")
        path_label.setMinimumWidth(120)
        self.lineEditSearch = QLineEdit()
        self.lineEditSearch.setPlaceholderText("Enter path to filter (optional)")
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.lineEditSearch)
        search_group_layout.addLayout(path_layout)
        
        # Keywords combo box
        keywords_layout = QHBoxLayout()
        keywords_label = QLabel("Keywords:")
        keywords_label.setMinimumWidth(120)
        self.combo = CheckableComboBox()
        
        # Load keywords from Excel spreadsheet
        try:
            df = pd.read_excel("2021-08-RFADT-Keywords.xlsx")
            keywords = df["Keywords"].tolist()
            self.combo.addItems(keywords)
            print(f"Loaded {len(keywords)} keywords")
        except Exception as e:
            print(f"Error loading keywords: {e}")
            # Add some default keywords if file not found
            self.combo.addItems(['keyword1', 'keyword2', 'keyword3'])
        
        keywords_layout.addWidget(keywords_label)
        keywords_layout.addWidget(self.combo)
        search_group_layout.addLayout(keywords_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.btnClear = QPushButton("Clear Table")
        self.btnClear.setMinimumSize(120, 35)
        self.btnClear.clicked.connect(self.clear_data)
        button_layout.addWidget(self.btnClear)
        
        self.btnSearch = QPushButton("Show Data")
        self.btnSearch.setMinimumSize(120, 35)
        self.btnSearch.clicked.connect(self.query_files)
        button_layout.addWidget(self.btnSearch)
        
        search_group_layout.addLayout(button_layout)
        
        search_group.setLayout(search_group_layout)
        main_layout.addWidget(search_group)